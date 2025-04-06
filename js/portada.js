let btnAgregar = document.getElementById("agregar");
let btnListado = document.getElementById("listado");
let btnEstadisticas = document.getElementById("estadisticas");

function irAgregar() {
    window.location.href = "../html/formulario.html";
}

function irListado() {
    window.location.href = "../html/lista_actividades.html"
}

btnAgregar.addEventListener("click", irAgregar);
btnListado.addEventListener("click", irListado);