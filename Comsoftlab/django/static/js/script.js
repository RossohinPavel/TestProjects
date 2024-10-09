const socket = new WebSocket('ws://' + window.location.host + '/ws/mail/')
let percent = ''


socket.onmessage = function(event) {
    // Распределяет работу исходя из наличия атрибутов в приходящем json
    let data = JSON.parse(event.data)
    if (data.pb) {
        updateProgressBar(data.pb)
    };
    if (data.mail) {
        updateTable(data.mail)
    };
    if (data.update) {
        location.reload(true);
    };
}


function updateProgressBar(data) {
    // Обновляет прогрессбар
    let pb = document.querySelector("#pb");
    if (data.message) {
        pb.innerText = data.message;
    };
    if (data.max) {
        pb.ariaValueMax = data.max;
        pb.ariaValueMin = data.current;
    };
    if (data.current) {
        pb.ariaValueNow = data.current;
        percent = String(data.current / pb.ariaValueMax * 100) + "%";
        pb.innerText = pb.innerText + ' ' + data.current + '/' + pb.ariaValueMax;
        pb.style.width = percent;
    }
}


function updateTable(data) {
    // Обновляет таблицу на странице
    let table = document.querySelector("#table");
    console.log(data);
    if (table.rows.length > 9) {
        table.querySelector('tr:last-child').remove();
    };
    table.insertAdjacentHTML('afterbegin', data);
}
