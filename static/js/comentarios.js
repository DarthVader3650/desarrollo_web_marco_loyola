const validateNombre = (nombre) => {
    if(!nombre) return false;
    let lengthValid = nombre.trim().length >= 3 && nombre.trim().length <= 80;
    return lengthValid;
}

const validateTexto = (texto) => {
    if(!texto) return false;
    let lenghtValid = texto.length >= 5 && texto.length <= 300;
    return lenghtValid;
}

document.addEventListener('DOMContentLoaded', () => {
    const btnAgregarComentario = document.getElementById('agregar_comentario');
    const listaComentariosDiv = document.getElementById('lista-comentarios');
    const actividadId = document.getElementById('actividad_id').value;

    function agregarComentario(comentario, prepend = false) {
        const comentarioDiv = document.createElement('div');
        comentarioDiv.className = 'comentario-item';
        comentarioDiv.innerHTML = `
            <p class="comentario-meta">
                <strong>${comentario.nombre}</strong> comentó el ${comentario.fecha}
            </p>
            <p class="comentario-texto">${comentario.texto}</p>`;
        if (prepend) {
            listaComentariosDiv.prepend(comentarioDiv); // Añade el comentario al principio
        } else {
            listaComentariosDiv.appendChild(comentarioDiv); // Añade el comentario al final
        }
    }

    async function cargarComentarios() {
        try {
            const response = await fetch(`http://127.0.0.1:5000/actividad/${actividadId}/comentarios`);
            if (!response.ok) {
                throw new Error('No se pudieron cargar los comentarios.');
            }
            const comentarios = await response.json();

            if (comentarios.length == 0) {
                listaComentariosDiv.innerHTML = '<p>¡Se el primero en comentar esta actividad!</p>';
            } else {
                comentarios.forEach(com => agregarComentario(com));
            }

        } catch (error) {
            listaComentariosDiv.innerHTML = `<p>${error.message}</p>`;
        }
    }

    async function validateForm(event) {
        event.preventDefault();

        let miForm = document.forms["nuevo_comentario"];
        let nombre_comentario = miForm["nombre"].value;
        let texto_comentario = miForm["comentario"].value;
        let validationBox = document.getElementById("val-box");
        let validationMessageElem = document.getElementById("val-msg");

        if(!validateNombre(nombre_comentario) || !validateTexto(texto_comentario)) {
            validationMessageElem.textContent = "Por favor, corrige los datos introducidos para enviar";
            validationBox.hidden = false;
            return
        }
        validationBox.hidden = true;
        btnAgregarComentario.disabled = true;

        const form_data = new FormData(miForm)

        try {
            const response = await fetch('http://127.0.0.1:5000/comentario', {
                method: "POST",
                body: form_data
            });

            if(!response.ok) {
                validationMessageElem.textContent = "Ocurrió un error"
                validationBox.hidden = false;
                throw new Error('Error del servidor');
            }

            const result = await response.json();
            if(result.status == "ok") {
                agregarComentario(result.comentario, true);
                miForm.reset();
            }
        } catch (error) {
            console.error('Falló la obtención de datos:', error);
        } finally {
            btnAgregarComentario.disabled = false;
        }
    }

    btnAgregarComentario.addEventListener('click', validateForm);
    cargarComentarios();
});