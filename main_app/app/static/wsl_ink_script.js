document.addEventListener("DOMContentLoaded", function () {
  var sendButton = document.getElementById("send");
  var fileInput = document.getElementById("file");
  var filenameInput = document.getElementById("filename");

  sendButton.onclick = function () {
    let file = fileInput.files[0];
    // if (!file) {
    //   alert("Файл не выбран");
    //   return
    // }
    let newFilename = filenameInput.value;

    if (file && newFilename) {
      let oldFilename = file.name;
      var ws = new WebSocket(
        "ws://localhost:8000/ws/file/?filename=" +
          encodeURIComponent(`${newFilename}:${oldFilename}`)
      );
      ws.binaryType = "arraybuffer";
      ws.onopen = function () {
        var reader = new FileReader();
        reader.onload = function (event) {
          ws.send(event.target.result);
        };
        reader.readAsArrayBuffer(file);
      };
      let filename_rec = "";
      ws.onmessage = function (event) {
        if (typeof event.data === "string") {
          // Предполагаем, что сервер отправляет URL в виде строки
          let downloadUrl = event.data;
          let downloadButton = document.createElement("button");
          downloadButton.textContent = "Скачать файл";
          downloadButton.onclick = function () {
            window.location.href = downloadUrl; // Перенаправление на URL для скачивания файла
            downloadButton.remove();
          };
          // Добавляем кнопку справа от кнопки отправить
          let sendButton = document.getElementById("send");
          sendButton.parentNode.insertBefore(downloadButton, sendButton.nextSibling);
        } else {
          alert(`Это не URL, а ${typeof event.data}`);
        }
      };
      ws.onerror = function (event) {
        console.error("Ошибка WebSocket: ", event);
      };
    } else {
      alert("Пожалуйста, выберите файл и введите имя файла.");
    }
  };
});
