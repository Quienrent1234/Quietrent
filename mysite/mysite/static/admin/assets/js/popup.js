//Multi dropdown
//https://codepen.io/gatoledo1/pen/wvmwgNp

let elem1 = document.getElementById('elem1')
let elem2 = document.getElementById('elem2')
let elem3 = document.getElementById('elem3')
let elem4 = document.getElementById('elem4')
let elem5 = document.getElementById('elem5')

elem1.addEventListener('click', function() {
    elem1.style.border = "solid 5px lightseagreen";
    elem2.style.border ="none";
});
elem2.addEventListener('click', function() {
    elem2.style.border = "solid 5px lightseagreen";
    elem1.style.border ="none";
});
elem3.addEventListener('click', function() {
    elem3.style.border = "solid 5px lightseagreen";
    elem4.style.border ="none";
    elem5.style.border ="none";
});
elem4.addEventListener('click', function() {
    elem4.style.border = "solid 5px lightseagreen";
    elem3.style.border ="none";
    elem5.style.border ="none";
});
elem5.addEventListener('click', function() {
    elem5.style.border = "solid 5px lightseagreen";
    elem3.style.border ="none";
    elem4.style.border ="none";
});

