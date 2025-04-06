let fila_1 = document.getElementById("fila_1");
let fila_2 = document.getElementById("fila_2");
let fila_3 = document.getElementById("fila_3");
let fila_4 = document.getElementById("fila_4");
let fila_5 = document.getElementById("fila_5");

fila_1.addEventListener("click", function() {
    window.location.href = "../html/actividad_1.html";
});

fila_2.addEventListener("click", function() {
    window.location.href = "../html/actividad_2.html";
});

fila_3.addEventListener("click", function() {
    window.location.href = "../html/actividad_3.html";
});

fila_4.addEventListener("click", function() {
    window.location.href = "../html/actividad_4.html";
});

fila_5.addEventListener("click", function() {
    window.location.href = "../html/actividad_5.html";
});

fila_1.addEventListener("mouseover", function() {
    fila_1.style.backgroundColor = '#4896b3';
    fila_1.style.cursor = 'pointer';
});

fila_1.addEventListener("mouseout", function() {
    fila_1.style.backgroundColor = '#ace8ff';
});

fila_2.addEventListener("mouseover", function() {
    fila_2.style.backgroundColor = '#4896b3';
    fila_2.style.cursor = 'pointer';
});

fila_2.addEventListener("mouseout", function() {
    fila_2.style.backgroundColor = 'rgb(205, 252, 255)';
});

fila_3.addEventListener("mouseover", function() {
    fila_3.style.backgroundColor = '#4896b3';
    fila_3.style.cursor = 'pointer';
});

fila_3.addEventListener("mouseout", function() {
    fila_3.style.backgroundColor = '#ace8ff';
});

fila_4.addEventListener("mouseover", function() {
    fila_4.style.backgroundColor = '#4896b3';
    fila_4.style.cursor = 'pointer';
});

fila_4.addEventListener("mouseout", function() {
    fila_4.style.backgroundColor = 'rgb(205, 252, 255)';
});

fila_5.addEventListener("mouseover", function() {
    fila_5.style.backgroundColor = '#4896b3';
    fila_5.style.cursor = 'pointer';
});

fila_5.addEventListener("mouseout", function() {
    fila_5.style.backgroundColor = '#ace8ff';
});