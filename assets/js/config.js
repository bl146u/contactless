"use strict";


(($) => {


    let WS = function() {

        let _host = "ws://bl146u.xyz:8099/";

        Object.defineProperty(this, "host", {
            get: () => {
                return _host;
            }
        });

    };


    $.extend(
        {
            WS: new WS()
        }
    );


})(jQuery);
