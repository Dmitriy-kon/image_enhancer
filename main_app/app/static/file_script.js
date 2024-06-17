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
    fetch("/text/file/", {
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

