"use strict";


(($) => {


    let add_log = (message, is_error) => {
        let item = $(`<div class="item">${message}</div>`);
        if (typeof is_error === "boolean") item.addClass(is_error ? "error" : "success");
        $("#logs").prepend(item);
    }


    $(() => {

        $("form").bind("submit", (event) => {
            event.preventDefault();
            let form = $(event.currentTarget).serializeArray(),
                data = {};
            form.forEach((item) => {
                data[item.name] = item.value;
            });
            $(event.currentTarget).find("input[type=text]").val("");
            socket.send(JSON.stringify(data));
        });

        let socket = new WebSocket("ws://localhost:8099/");

        socket.onmessage = function(event) {
            let data = JSON.parse(event.data);
            add_log(data.message);
        };

        socket.onclose = function(e) {
            add_log("Chat socket closed unexpectedly", true);
        };

    })

})(jQuery);