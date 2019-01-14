class PredictServer {
    static async sendToServer (imageData, successCallback) {
        var formData = new FormData();
        formData.append("image", new Blob([imageData]));
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
                successCallback(json)
            } else {
                console.error(response.status);
            }
        } catch(err) {
            console.error(err);
        }
    }
};

PredictServer.url = "http://localhost:5000/predict";
