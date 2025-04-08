// Código sacado de W3School.

// Modal 1
let modal = document.getElementById('myModal');
let img = document.getElementById('img_1');
let modalImg = document.getElementById("img01");
let captionText = document.getElementById("caption");
let span = document.querySelectorAll("#myModal .close")[0];

img.onclick = function() {
  modal.style.display = "block";
  modalImg.src = this.src;
  captionText.innerHTML = this.alt;
}

span.onclick = function() {
  modal.style.display = "none";
}

// Modal 2
let modal_2 = document.getElementById('myModal_2');
let img_2 = document.getElementById('img_2');
let modalImg_2 = document.getElementById("img02");
let captionText_2 = document.getElementById("caption_2");
let span_2 = document.querySelectorAll("#myModal_2 .close")[0];

img_2.onclick = function() {
  modal_2.style.display = "block";
  modalImg_2.src = this.src;
  captionText_2.innerHTML = this.alt;
}

span_2.onclick = function() {
  modal_2.style.display = "none";
}