document.addEventListener("DOMContentLoaded", function () {
  let form = document.getElementById("file-upload-form");

  function collectMetadata() {
    return {
      grayscale: document.getElementById("grayscale").checked,
      scale: {
        width: parseInt(document.getElementById("scaleWidth").value, 10),
        height: parseInt(document.getElementById("scaleHeight").value, 10),
      },
      saturation: parseInt(document.getElementById("saturation").value, 10),
    };
  }

  form.onsubmit = function (event) {
    event.preventDefault();
    let fileInput = document.getElementById("file");
    let filenameInput = document.getElementById("filename");
    let file = fileInput.files[0];
    let newFilename = filenameInput.value.trim();
    let oldFilename = file ? file.name : "";

    if (!file || !newFilename) {
      alert("Файл или имя файла не выбраны");
      return;
    }


      
    let metadata = collectMetadata();

    console.log(metadata);

    let formData = new FormData();
    formData.append("file", file);
    formData.append("filename", newFilename);
    formData.append("metadata", JSON.stringify(metadata));
    fetch("/image/", {
      method: "POST",
      body: formData,
    })
      .then((response) => {
        return response.text();
      })
      .then((data) => {
        console.log(data);
        // Обработайте ответ сервера здесь
      })
      .catch((error) => {
        console.error(error);
      });

    let ws = new WebSocket(
      "ws://localhost:8000/ws/file/?filename=" +
        encodeURIComponent(`${newFilename}:${oldFilename}`)
    );

    ws.onopen = function () {
      console.log("WebSocket соединение установлено.");
    };

    ws.onmessage = function (event) {
      if (typeof event.data === "string") {
        // Предполагаем, что сервер отправляет URL в виде строки
        let downloadUrl = event.data;
        let buttonsContainer = document.getElementById("mybuttons");
        let downloadButton = document.createElement("button");
        downloadButton.textContent = "Скачать файл";
        downloadButton.onclick = function () {
          window.location.href = downloadUrl; // Перенаправление на URL для скачивания файла
          downloadButton.remove(); // Удаление кнопки после нажатия
        };
        // Добавляем кнопку справа от кнопки отправить
        buttonsContainer.appendChild(downloadButton);
      } else {
        alert(`Это не URL, а ${typeof event.data}`);
      }
    };

    ws.onerror = function (error) {
      console.error("WebSocket ошибка: " + error.message);
    };

    ws.onclose = function (event) {
      console.log("WebSocket соединение закрыто: " + event.code);
    };
  };
});

let originalWidth, originalHeight;

document.getElementById('file').addEventListener('change', function(event) {
  let file = event.target.files[0];
  if (file && file.type.startsWith('image/')) {
    let img = new Image();
    img.onload = function() {
      originalWidth = this.width;
      originalHeight = this.height;
      document.getElementById('scaleWidth').value = originalWidth;
      document.getElementById('scaleHeight').value = originalHeight;
    };
    img.src = URL.createObjectURL(file);
  }
});

function updateProportionalSize(inputId, originalSize) {
  if (document.getElementById('proportional').checked) {
    let scaleWidth = document.getElementById('scaleWidth');
    let scaleHeight = document.getElementById('scaleHeight');
    let ratio = originalWidth / originalHeight;
    
    if (inputId === 'scaleWidth') {
      let newWidth = parseInt(scaleWidth.value, 10);
      scaleHeight.value = Math.round(newWidth / ratio);
    } else if (inputId === 'scaleHeight') {
      let newHeight = parseInt(scaleHeight.value, 10);
      scaleWidth.value = Math.round(newHeight * ratio);
    }
  }
}

document.getElementById('scaleWidth').addEventListener('input', function() {
  updateProportionalSize('scaleWidth', originalWidth);
});

document.getElementById('scaleHeight').addEventListener('input', function() {
  updateProportionalSize('scaleHeight', originalHeight);
});