"use strict";


(($) => {


    let add_log = (name, message, is_error) => {
        let item = $(`<div class="item"><b>${name}:</b> ${message}</div>`);
        if (typeof is_error === "boolean") item.addClass(is_error ? "error" : "success");
        $("#logs > .item.empty").remove();
        $("#logs").prepend(item);
    }


    $(() => {

        let field_message = $("input[name=message]"),
            field_file = $("input[name=file]");

        let chat = new WebSocket(`${$.WS.host}send/`);
        chat.onmessage = (event) => {
            let data = JSON.parse(event.data);
            add_log(data.name, data.message);
        };
        chat.onclose = (e) => {
            add_log("admin", "Chat socket closed unexpectedly", true);
        };

        $("form.chat").bind("submit", (event) => {
            event.preventDefault();
            let form = $(event.currentTarget).serializeArray(),
                data = {};
            form.forEach((item) => {
                data[item.name] = item.value;
            });
            let is_error = false;
            if (field_message.val() === "") {
                is_error = true;
                field_message.addClass("error");
            } else {
                field_message.removeClass("error");
            }
            if (!is_error) {
                chat.send(JSON.stringify(data));
                field_message.val("");
            }
            field_message.focus();
        });

        $("form.profile").bind("submit", (event) => {
            event.preventDefault();
            let signout = new WebSocket(`${$.WS.host}sign-out/`);
            signout.onmessage = (event) => {
                window.location.reload();
            }
            signout.onopen = (event) => {
                signout.send(JSON.stringify({}))
            }
        });

        let uploader = new $.Uploader((data) => {
            let files_block = $("#files"),
                file_block = $(`#${data.id}`);
            files_block.children(".item.empty").remove();
            if (!file_block.length) {
                file_block = $(`<div id="${data.id}" class="item">
                    <div class="info"><div class="user"><span></span></div><div class="name"><span></span></div><div class="size"><span></span></div></div>
                    <div class="progress"><span></span></div>
                </div>`);
                files_block.append(file_block);
            }
            file_block.find(".info > .user > span").text(data.user);
            file_block.find(".info > .name > span").text(data.name);
            file_block.find(".info > .size > span").text(`${data.size} / ${data.total}`);
            file_block.find(".progress > span").width(`${data.size / data.total * 100}%`);
        });

        $("form.upload").bind("submit", (event) => {
            event.preventDefault();
            $(field_file[0].files).each((index, file) => {
                uploader.send(file);
            });
        });
        field_file.bind("change", (event) => {
            event.preventDefault();
            $("form.upload").submit();
        });

    })

})(jQuery);