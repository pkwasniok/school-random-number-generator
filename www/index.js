var label_number_1 = document.getElementById("number-1");
var label_number_2 = document.getElementById("number-2");

fetch("http://127.0.0.1:5000/", { credentials: 'same-origin' }).then((response) => {
    return response.json();
}).then((data) => {
    label_number_1.innerHTML = data[0];
    label_number_2.innerHTML = data[1];
}).catch(() => {
    console.log("Something went wrong while fetching data from API")
})