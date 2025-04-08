const contactos = ["WhatsApp", "Telegram", "X", "Instagram", "TikTok", "Facebook"];
const temas = ["Música", "Deporte", "Ciencia", "Religíon", "Política", "Tecnología", "Juegos", "Baile", "Comida", "Otro"];
const fotos = document.getElementById("foto");
const otraFoto = document.getElementById("otra-foto");
let btnVolver = document.getElementById("volver");
let btnAgregarFoto = document.getElementById("agregarFoto");
let conteoFotos = 0;

function volver() {
    window.location.href = "../html/portada.html";
};
btnVolver.addEventListener("click", volver);

btnAgregarFoto.addEventListener("click", function() {
    if (conteoFotos + fotos.files.length >= 5) {
        alert("No puedes agregar más de 5 fotos.");
        return;
    }

    otraFoto.style.display = "block";
    btnAgregarFoto.style.display = "none";

    conteoFotos++;
})

function revisaCheck(element) {
    if (element.checked) {
        document.getElementById(element.name).style.display = "block";
    } else {
        document.getElementById(element.name).style.display = "none";
    }
}

const seleccionTema = () => {
    let temaSeleccionado = document.getElementById("tema");

    for (const tema of temas) {
        let option = document.createElement("option");
        option.value = tema;
        option.text = tema;
        temaSeleccionado.appendChild(option);
    };
};

function changeTema() {
    const temaEscogido = document.getElementById("tema");
    const infoLabelTema = document.querySelector("label[for='otro']");
    const infoTextTema = document.getElementById("otro");

    if (temaEscogido.value == "Otro") {
        infoLabelTema.style.display = "block";
        infoTextTema.style.display = "block";
    } else {
        infoLabelTema.style.display = "none";
        infoTextTema.style.display = "none";
    }
};

document.getElementById("tema").addEventListener("change", changeTema);

document.addEventListener('DOMContentLoaded', () => {
    seleccionTema();
});