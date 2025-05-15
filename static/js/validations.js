const validateName = (name) => {
    if(!name) return false;
    let lengthValid = name.trim().length >= 4 && name.trim().length <= 200;
    return lengthValid;
}

const validateEmail = (email) => {
    if (!email) return false;
    let lengthValid = email.length > 15 && email.length <= 100;
  
    // validamos el formato
    let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    let formatValid = re.test(email);
  
    // devolvemos la lógica AND de las validaciones.
    return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
    if (phoneNumber) {
        // validación de longitud
        let lengthValid = phoneNumber.length >= 8;
    
        // validación de formato
        let re = /^(\+56)?(\s?)((2|3|4|5|6|7|8|9)(\s?)\d{8})$/;
        let formatValid = re.test(phoneNumber);
    
        // devolvemos la lógica AND de las validaciones.
        return lengthValid && formatValid;
    } else {
        return true
    }
};

const validateSector = (sector) => {
    let lenghtValid = sector.length >= 0 && sector.length <= 100;

    return lenghtValid;
}

const validateDataTime = (datatime) => {
    if (!datatime) return false;

    let re = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
    let formatValid = re.test(datatime);

    return formatValid;
}

const validateDataTimeEnd = (datatime) => {
    if (!datatime) return true;
    const datatimeBegin = document.getElementById("inicio").value;
    if (!datatimeBegin) return false;
    const dateEnd = new Date(datatime);
    const dateBegin = new Date(datatimeBegin);
    return dateEnd > dateBegin;
}

const vaildateRegion = (region) => {
    if (!region) return false;
    return true;
}

const validateComuna = (comuna) => {
    if (!comuna) return false;
    return true;
}

const validateFotos = (files) => {
    if (!files) return false;

    // validación del número de archivos
    let lengthValid = 1 <= files.length && files.length <= 5;

    // validación del tipo de archivo
    let typeValid = true;

    for (const file of files) {
        // el tipo de archivo debe ser "image/<foo>"
        let fileFamily = file.type.split("/")[0];
        typeValid &&= fileFamily == "image";
    }
    
    // devolvemos la lógica AND de las validaciones.
    return lengthValid && typeValid;
}

const validateOtraFoto = (foto) => {
    let btnAgregarFoto = document.getElementById("agregarFoto");
    if (btnAgregarFoto.style.display == "none") {

        if (!foto || foto.length == 0) return false;

        const archivo = foto[0];
        const tiposImagenPermitidos = ['image/jpeg', 'image/png', 'image/gif'];
        const typeValid = tiposImagenPermitidos.includes(archivo.type);
        return typeValid;
    } else return true;
};

const validateInfoContacto = () => {
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    let formValido = true;

    let checkedCount = 0;
    checkboxes.forEach(cb => {
        if (cb.checked) {
            checkedCount++;
        }
    });

    checkboxes.forEach(cbox => {
        if (cbox.checked) {
            if (checkedCount > 5) {
                formValido = false;
            }
            const inputTexto = document.getElementById(cbox.name);
            if (inputTexto.value.length < 4 || inputTexto.value.length > 50) {
                formValido = false;
            }
        }
    });
    return formValido;
}

const validateOtro = (otro) => {
    const tema = document.getElementById("tema").value;
    if (tema === "Otro") {
        return otro.length >= 3 && otro.length <= 15;
    }
    return true;
}

const validateTema = (tema) => {
    if (!tema) return false;
    return true;
}

// const validateContactar = (formas) => {}

const validateForm = () => {
    let miForm = document.forms["nueva_actividad"];
    let nombre = miForm["nombre"].value;
    let email = miForm["email"].value;
    let telefono = miForm["teléfono"].value;
    let sector = miForm["sector"].value;
    let fecha_inicio = miForm["inicio"].value;
    let fecha_termino = miForm["término"].value;
    let region = miForm["región"].value;
    let comuna = miForm["comuna"].value;
    let fotos = miForm["foto"].files;
    let otraFoto = miForm["otra-foto"].files;
    let otro = miForm["otro"].value;
    let tema = miForm["tema"].value;

    // variables auxiliares de validación y función.
    let invalidInputs = [];
    let isValid = true;
    const setInvalidInput = (inputName) => {
        invalidInputs.push(inputName);
        isValid &&= false;
    };

    // lógica de validación
    if (!validateName(nombre)) setInvalidInput("Nombre");
    if (!validateEmail(email)) setInvalidInput("Email");
    if (!validatePhoneNumber(telefono)) setInvalidInput("Teléfono");
    if (!validateSector(sector)) setInvalidInput("Sector");
    if (!validateDataTime(fecha_inicio)) setInvalidInput("Fecha de inicio");
    if (!validateDataTimeEnd(fecha_termino)) setInvalidInput("Fecha de término");
    if (!vaildateRegion(region)) setInvalidInput("Region");
    if (!validateComuna(comuna)) setInvalidInput("Comuna");
    if (!validateFotos(fotos)) setInvalidInput("Fotos: Máximo 5");
    if (!validateOtraFoto(otraFoto)) setInvalidInput("La otra foto añadida");
    if (!validateInfoContacto()) setInvalidInput("Información de contacto: Máximo 5");
    if (!validateOtro(otro)) setInvalidInput("Otro");
    if (!validateTema(tema)) setInvalidInput("Tema");

    // finalmente mostrar la validación
    let validationBox = document.getElementById("val-box");
    let validationMessageElem = document.getElementById("val-msg");
    let validationListElem = document.getElementById("val-list");

    if (!isValid) {
        validationListElem.textContent = "";
        // agregar elementos inválidos al elemento val-list.
        for (input of invalidInputs) {
          let listElement = document.createElement("li");
          listElement.innerText = input;
          validationListElem.append(listElement);
        }
        // establecer val-msg
        validationMessageElem.innerText = "Los siguientes campos son inválidos:";
    
        // aplicar estilos de error
        validationBox.style.backgroundColor = "#ffdddd";
        validationBox.style.borderLeftColor = "#f44336";
    
        // hacer visible el mensaje de validación
        validationBox.hidden = false;
      } else {
        // Ocultar el formulario
        miForm.style.display = "none";
    
        // establecer mensaje de éxito
        validationMessageElem.innerText = "¿Está seguro que desea agregar esta actividad?";
        validationListElem.textContent = "";
    
        // aplicar estilos de éxito
        validationBox.style.backgroundColor = "#87ceeb";
        validationBox.style.borderLeftColor = "#0063d5";
    
        // Agregar botones para enviar el formulario o volver
        let submitButton = document.createElement("button");
        submitButton.innerText = "Si, estoy seguro";
        submitButton.style.marginRight = "10px";
        submitButton.addEventListener("click", () => {
            validationMessageElem.innerText = "¡Hemos recibido su información, muchas gracias y suerte en su actividad!";
            validationListElem.removeChild(submitButton);
            validationListElem.removeChild(backButton);
            validationListElem.appendChild(volverButton);
            miForm.submit();
        });
    
        let backButton = document.createElement("button");
        backButton.innerText = "No, no estoy seguro";
        backButton.addEventListener("click", () => {
          // Mostrar el formulario nuevamente
          miForm.style.display = "block";
          validationBox.hidden = true;
        });

        let volverButton = document.createElement("button");
        volverButton.innerText = "Volver al menu";
        volverButton.addEventListener("click", () => {
            window.location.href = "../html/portada.html";
        })
    
        validationListElem.appendChild(submitButton);
        validationListElem.appendChild(backButton);
    
        // hacer visible el mensaje de validación
        validationBox.hidden = false;
    }
}

let botonEnviar = document.getElementById("agregar");
botonEnviar.addEventListener("click", validateForm);