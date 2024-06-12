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
        if (typeof event.data == "string") {
          filename_rec = event.data;
          console.log(
            `Сервер ответил: ${filename_rec} and type ${typeof event.data}`
          );
        } else {
          let arrayBuffer = event.data;
          let blob = new Blob([arrayBuffer], {
            type: "application/octet-stream",
          });

          let url = window.URL.createObjectURL(blob);
          let downloadLink = document.createElement("a");

          downloadLink.href = url;
          downloadLink.download = filename_rec;
          downloadLink.textContent = "Скачать " + filename_rec;
          document.body.appendChild(downloadLink);
          downloadLink.click();
          document.body.removeChild(downloadLink);
        }
        console.log("Сервер ответил: ", event.data);
        // window.URL.revokeObjectURL(url);
        // Обработайте ответ сервера здесь
      };
      ws.onerror = function (event) {
        console.error("Ошибка WebSocket: ", event);
      };
    } else {
      alert("Пожалуйста, выберите файл и введите имя файла.");
    }
  };
});
