// Basado en el modal de W3School
document.addEventListener('DOMContentLoaded', function() {
    const fotosActividad = document.querySelectorAll('img')
    let modal = document.getElementById('myModal');
    let imagenZoom = document.createElement('img');
    imagenZoom.className = "modal-content";
    let span = document.querySelectorAll("#myModal .close")[0];

    fotosActividad.forEach(foto => {
      foto.addEventListener('click', function() {
        imagenZoom.src = foto.src;
        imagenZoom.alt = foto.alt;
        modal.style.display = "block";
        modal.appendChild(imagenZoom);
      })
    })

    span.onclick = function() {
      modal.style.display = "none";
      modal.removeChild(imagenZoom);
    }
})