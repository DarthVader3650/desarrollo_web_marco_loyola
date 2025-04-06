let btnAgregar = document.getElementById("agregar");
let btnListado = document.getElementById("listado");
let btnEstadisticas = document.getElementById("estadisticas");

function irAgregar() {
    window.location.href = "../html/formulario.html";
}

btnAgregar.addEventListener("click", irAgregar);