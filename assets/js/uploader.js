"use strict";


(($) => {

    let FileSlicer = function(file) {
        this.sliceSize = 1024 * 1024;
        // this.sliceSize = 512;
        this.slices = Math.ceil(file.size / this.sliceSize);
        this.currentSlice = 0;
        this.getNextSlice = function() {
            let start = this.currentSlice * this.sliceSize,
                end = Math.min((this.currentSlice+1) * this.sliceSize, file.size);
            ++this.currentSlice;
            return file.slice(start, end);
        }
    }


    $.extend({


        Uploader: function(callback) {

            let files = {},
                ws = new WebSocket(`${$.WS.host}files/`);

            ws.onmessage = (event) => {
                let data = JSON.parse(event.data);
                if (data.uuid && files[data.uuid]) upload(data);
                if (typeof callback === "function") callback(data);
            }

            let uuid4 = () => {
                return ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
                    (c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16)
                );
            }

            let upload = (data) => {
                let file = files[data.uuid],
                    fs = new FileSlicer(file);
                for (let i = 0; i < fs.slices; ++i) {
                    let slice = fs.getNextSlice();
                    ws.send(new Blob([slice, `\n${data.id}`]));
                }
            }

            this.send = (file) => {
                let uuid = uuid4();
                files[uuid] = file;
                ws.send(
                    JSON.stringify({
                        uuid: uuid,
                        name: file.name,
                        size: file.size
                    })
                );
            }

        }


    });


})(jQuery);
