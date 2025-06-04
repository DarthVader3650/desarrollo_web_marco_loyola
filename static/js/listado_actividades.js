document.addEventListener('DOMContentLoaded', function() {
    const filasActividad = document.querySelectorAll('tbody tr');

    filasActividad.forEach(fila => {
        fila.addEventListener('click', function() {
            const actividadId = this.dataset.id;
            if (actividadId) {
                window.location.href = `/actividad/${actividadId}`;
            } else {
                console.error('No se encontró el ID de la actividad para esta fila.');
            }
        });
    });
});