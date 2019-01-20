class PredictServer {
    static async sendToServer (file, completionCallback) {
        var formData = new FormData();
        formData.append("image", new Blob([file]));
        formData.append("imagename", file.name);
        var data = { // Your POST endpoint
            method: 'POST',
            // headers: {
            //     "Content-Type": ""
            // },
            // body: imageData // This is your file object or URL
            body: formData // This is your file object or URL
        }
        try {
            var response = await fetch(PredictServer.url, data);
            console.log(response);
            if (response.ok) {
                var json = await response.json();
                console.log(json);
                if (json["error"] == false) {
                    completionCallback(json, true)
                } else {
                    completionCallback(json, false)
                }
            } else {
                console.error(response.status);
                completionCallback(json, false)
            }
        } catch(err) {
            console.error(err);
            completionCallback(json, false)
        }
    }
};

PredictServer.url = "http://localhost:5000/predict";
