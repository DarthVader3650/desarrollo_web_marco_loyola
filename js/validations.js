const validateName = (name) => {
    if(!name) return false;
    let lengthValid = 200 >= name.trim().length >= 4;
    return lengthValid;
}

const validateEmail = (email) => {
    if (!email) return false;
    let lengthValid = 100 >= email.length > 15;
  
    // validamos el formato
    let re = /^[\w.]+@[a-zA-Z_]+?\.[a-zA-Z]{2,3}$/;
    let formatValid = re.test(email);
  
    // devolvemos la lógica AND de las validaciones.
    return lengthValid && formatValid;
};

const validatePhoneNumber = (phoneNumber) => {
    // validación de longitud
    let lengthValid = phoneNumber.length >= 8;
  
    // validación de formato
    let re = /^(\+56)?(\s?)((2|3|4|5|6|7|8|9)(\s?)\d{8})$/;
    let formatValid = re.test(phoneNumber);
  
    // devolvemos la lógica AND de las validaciones.
    return lengthValid && formatValid;
};

const validateSector = (sector) => {
    let lenghtValid = 100 >= sector.length > 0;

    return lenghtValid;
}

const validateDataTime = (datatime) => {
    if (!datatime) return false;

    let re = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
    let formatValid = re.test(datatime);

    return formatValid;
}

const validateDataTimeEnd = (datatime) => {
    const datatimeBegin = document.getElementById("inicio");

    let re = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/;
    let formatValid = re.test(datatime);

    if (datatime > datatimeBegin.value) {
        return formatValid
    } else {
        return false
    }
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

const validateInfoContacto = (info) => {
    let lenghtValid = 4 <= info.length <= 50;

    return lenghtValid;
}

const validateOtro = (otro) => {
    const tema = document.getElementById("tema")

    if (tema.value == "Otro") {
        if (!otro) return false;
        else {
            let lenghtValid = 3 <= otro.length <= 15;
            return lenghtValid;
        }
    } else return true;
}

const validateTema = (temas) => {
    if (!temas) return false;
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
    let fotos = miForm["foto"].value;
    let info_contacto = miForm["info_contacto"].value;
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
    if (!validateName(nombre)) {
        setInvalidInput("Nombre");
    }
    if (!validateEmail(email)) {
        setInvalidInput("Email");
    }
    if (!validatePhoneNumber(telefono)) {
        setInvalidInput("Teléfono");
    }
    if (!validateSector(sector)) {
        setInvalidInput("Sector");
    }
    if (!validateDataTime(fecha_inicio)) {
        setInvalidInput("Fecha de inicio");
    }
    if (!validateDataTimeEnd(fecha_termino)) {
        setInvalidInput("Fecha de término");
    }
    if (!vaildateRegion(region)) {
        setInvalidInput("Region");
    }
    if (!validateComuna(comuna)) {
        setInvalidInput("Comuna");
    }
    if (!validateFotos(fotos)) {
        setInvalidInput("Fotos");
    }
    if (!validateInfoContacto(info_contacto)) {
        setInvalidInput("Información de contacto");
    }
    if (!validateOtro(otro)) {
        setInvalidInput("Otro");
    }
    if (!validateTema(tema)) {
        setInvalidInput("Tema");
    }

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
        validationMessageElem.innerText = "¡Formulario válido! ¿Deseas enviarlo o volver?";
        validationListElem.textContent = "";
    
        // aplicar estilos de éxito
        validationBox.style.backgroundColor = "#ddffdd";
        validationBox.style.borderLeftColor = "#4CAF50";
    
        // Agregar botones para enviar el formulario o volver
        let submitButton = document.createElement("button");
        submitButton.innerText = "Enviar";
        submitButton.style.marginRight = "10px";
        submitButton.addEventListener("click", () => {
          // miForm.submit();
          // no tenemos un backend al cual enviarle los datos
        });
    
        let backButton = document.createElement("button");
        backButton.innerText = "Volver";
        backButton.addEventListener("click", () => {
          // Mostrar el formulario nuevamente
          miForm.style.display = "block";
          validationBox.hidden = true;
        });
    
        validationListElem.appendChild(submitButton);
        validationListElem.appendChild(backButton);
    
        // hacer visible el mensaje de validación
        validationBox.hidden = false;
    }
}

let botonEnviar = document.getElementById("agregar");
botonEnviar.addEventListener("click", validateForm);