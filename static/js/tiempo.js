const horaInicio = document.getElementById("inicio");
const horaFinal = document.getElementById("término");
const fechaActual = new Date();
const fechaActualPlus = new Date();
fechaActualPlus.setHours(fechaActualPlus.getHours() + 3);

function formatearDatetimeLocal(fecha) {
    const anio = fecha.getFullYear();
    const mes = String(fecha.getMonth() + 1).padStart(2, '0');
    const dia = String(fecha.getDate()).padStart(2, '0');
    const horas = String(fecha.getHours()).padStart(2, '0');
    const minutos = String(fecha.getMinutes()).padStart(2, '0');
    return `${anio}-${mes}-${dia}T${horas}:${minutos}`;
}

horaInicio.value = formatearDatetimeLocal(fechaActual);
horaFinal.value = formatearDatetimeLocal(fechaActualPlus);