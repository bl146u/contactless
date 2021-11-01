"use strict";


(($) => {


    let add_log = (name, message, is_error) => {
        let item = $(`<div class="item"><b>${name}:</b> ${message}</div>`);
        if (typeof is_error === "boolean") item.addClass(is_error ? "error" : "success");
        $("#logs").prepend(item);
    }


    $(() => {

        let field_name = $("input[name=name]"),
            field_message = $("input[name=message]");

        $("form").bind("submit", (event) => {
            event.preventDefault();
            let form = $(event.currentTarget).serializeArray(),
                data = {};
            form.forEach((item) => {
                data[item.name] = item.value;
            });
            let is_error = false;
            if (field_name.val() === "") {
                is_error = true;
                field_name.addClass("error");
            } else {
                field_name.removeClass("error");
            }
            if (field_message.val() === "") {
                is_error = true;
                field_message.addClass("error");
            } else {
                field_message.removeClass("error");
            }
            if (!is_error) {
                socket.send(JSON.stringify(data));
                field_message.val("");
            }
            field_message.focus();
        });

        if (field_name.val() === "") field_name.focus();

        let socket = new WebSocket("ws://192.168.1.101:8099/");

        socket.onmessage = (event) => {
            let data = JSON.parse(event.data);
            add_log(data.name, data.message);
        };

        socket.onclose = (e) => {
            add_log("admin", "Chat socket closed unexpectedly", true);
        };

    })

})(jQuery);