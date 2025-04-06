const contactos = ["WhatsApp", "Telegram", "X", "Instagram", "TikTok", "Facebook"];
const temas = ["Música", "Deporte", "Ciencia", "Religíon", "Política", "Tecnología", "Juegos", "Baile", "Comida", "Otro"];
let btnVolver = document.getElementById("volver");

function volver() {
    window.location.href = "../html/portada.html";
}

const formatoContacto = () => {
    let contactoSeleccionado = document.getElementById("contactar")

    for (const contacto of contactos) {
        let option = document.createElement("option");
        option.value = contacto;
        option.text = contacto;
        contactoSeleccionado.appendChild(option);
    }
};

function changeApp() {
    const contactoEscogido = document.getElementById("contactar");
    const infoLabel = document.querySelector("label[for='info_contacto']");
    const infoText = document.getElementById("info_contacto");
    
    if (contactoEscogido.value !== "") {
        infoLabel.style.display = "block";
        infoText.style.display = "block";
    } else {
        infoLabel.style.display = "none";
        infoText.style.display = "none";
    }
}

const seleccionTema = () => {
    let temaSeleccionado = document.getElementById("tema");
    let divOtro = null;

    for (const tema of temas) {
        let option = document.createElement("option");
        option.value = tema;
        option.text = tema;
        temaSeleccionado.appendChild(option);
    }
}

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
}

document.getElementById("contactar").addEventListener("change", changeApp);
document.getElementById("tema").addEventListener("change", changeTema);

window.onload = () => {
    formatoContacto();
    seleccionTema();
};

btnVolver.addEventListener("click", volver);