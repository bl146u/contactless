"use strict";


(($) => {


    $(() => {

        let field_username = $(".auth > form > input[name=username]"),
            field_password = $(".auth > form > input[name=password]");

        $(".auth > form").bind("submit", (event) => {
            event.preventDefault();
            let form = $(event.currentTarget).serializeArray(),
                data = {};
            form.forEach((item) => {
                data[item.name] = item.value;
            });
            let is_error = false;
            if (field_username.val() === "") {
                is_error = true;
                field_username.addClass("error");
            } else {
                field_username.removeClass("error");
            }
            if (field_password.val() === "") {
                is_error = true;
                field_password.addClass("error");
            } else {
                field_password.removeClass("error");
            }
            if (!is_error) {
                let signin = new WebSocket(`${$.WS.host}sign-in/`);
                signin.onmessage = (event) => {
                    let data = JSON.parse(event.data);
                    if (data["sessionid"]) {
                        $.cookie(
                            "sessionid",
                            data["sessionid"],
                            {
                                "path": "/",
                                "expires": data["expires"] / 86400
                            }
                        );
                        window.location.reload();
                    }
                };
                signin.onopen = (event) => {
                    signin.send(JSON.stringify(data));
                };
            }
        });

    })

})(jQuery);