"use strict";


(($) => {


    $(() => {

        let signin_field_username = $(".auth > form > input[name=username]"),
            signin_field_password = $(".auth > form > input[name=password]"),
            signup_field_username = $(".sign-up > input[name=username]"),
            signup_field_password = $(".sign-up > input[name=password]");

        $(".auth > form").bind("submit", (event) => {
            event.preventDefault();
            let form = $(event.currentTarget).serializeArray(),
                data = {};
            form.forEach((item) => {
                data[item.name] = item.value;
            });
            let is_error = false;
            if (signin_field_username.val() === "") {
                is_error = true;
                signin_field_username.addClass("error");
            } else {
                signin_field_username.removeClass("error");
            }
            if (signin_field_password.val() === "") {
                is_error = true;
                signin_field_password.addClass("error");
            } else {
                signin_field_password.removeClass("error");
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

        $(".sign-up").bind("submit", (event) => {
            event.preventDefault();
            let form = $(event.currentTarget).serializeArray(),
                data = {};
            form.forEach((item) => {
                data[item.name] = item.value;
            });
            let is_error = false;
            if (signup_field_username.val() === "") {
                is_error = true;
                signup_field_username.addClass("error");
            } else {
                signup_field_username.removeClass("error");
            }
            if (signup_field_password.val() === "") {
                is_error = true;
                signup_field_password.addClass("error");
            } else {
                signup_field_password.removeClass("error");
            }
            if (!is_error) {
                let signin = new WebSocket(`${$.WS.host}sign-up/`);
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