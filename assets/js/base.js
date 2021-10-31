"use strict";


(($) => {

    $(() => {

        let socket = new WebSocket("ws://localhost:8099/ws/");

        socket.onopen = (event) => {
            socket.send("Привет");
            console.info("WS connected:", event.type)
        };
        socket.onclose = (event) => {
            if (event.wasClean) {
                console.info("WS closed clear:", event.type);
            } else {
                console.info("WS lost connection:", event.type);
            }
        };
        socket.onmessage = (event) => {
            console.info("WS data received:", event.data);
        };
        socket.onerror = (error) => {
            console.info("WS error:", error.message);
        };

    })

})(jQuery);