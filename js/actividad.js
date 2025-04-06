let btn_menu = document.getElementById("volverPortada");
let btnListado = document.getElementById("volverListado");

btnListado.addEventListener("click", function() {
    window.location.href = "../html/lista_actividades.html";
});

btn_menu.addEventListener("click", function() {
    window.location.href = "../html/portada.html";
});