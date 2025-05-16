// Basado en el modal de W3School

// Modal 1
let modal = document.getElementById('myModal');
let img = document.getElementById('img_1');
let imagenZoom = document.createElement('img');
imagenZoom.className = "modal-content";
imagenZoom.src = img.src;
imagenZoom.alt = img.alt;
let span = document.querySelectorAll("#myModal .close")[0];

img.onclick = function() {
  modal.style.display = "block";
  modal.appendChild(imagenZoom);
}

span.onclick = function() {
  modal.style.display = "none";
  modal.removeChild(imagenZoom);
}

// Modal 2
let modal_2 = document.getElementById('myModal_2');
let img_2 = document.getElementById('img_2');
let imagenZoom2 = document.createElement('img');
imagenZoom2.className = "modal-content";
imagenZoom2.src = img_2.src;
imagenZoom2.alt = img_2.alt;
let span_2 = document.querySelectorAll("#myModal_2 .close")[0];

img_2.onclick = function() {
  modal_2.style.display = "block";
  modal_2.appendChild(imagenZoom2);
}

span_2.onclick = function() {
  modal_2.style.display = "none";
  modal_2.removeChild(imagenZoom2);
}