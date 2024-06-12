document.addEventListener('DOMContentLoaded', function() {
    var form = document.getElementById('file-upload-form');
    form.onsubmit = function(event) {
        event.preventDefault();
        var formData = new FormData(form);
        fetch('/text/file/', {
            method: 'POST',
            body: formData
        }).then(response => {
            return response.text();
        }).then(data => {
            console.log(data);
            // Обработайте ответ сервера здесь
        }).catch(error => {
            console.error(error);
        });
    };
});
