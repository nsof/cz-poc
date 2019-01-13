class PredictServer {
    static sendToServer(imageData) {
        var formData = new FormData();
        formData.append("image", new Blob([imageData]));
        fetch(PredictServer.url, { // Your POST endpoint
            method: 'POST',
            // headers: {
            //     "Content-Type": ""
            // },
            // body: imageData // This is your file object or URL
            body: formData // This is your file object or URL
        }).then(
            response => response
        ).then(
            success => console.log(success) // Handle the success response object
        ).catch(
            error => console.log(error) // Handle the error response object
        );        
    }
};

PredictServer.url = "http://localhost:5000/predict";
