$(document).ready(function() {
  const btn1 = $("#btn-dir");
  const btn2 = $("#btn-com");
  const btn3 = $("#btn-addcom");
  const btn4 = $("#btn-vid");
  const btn5 = $(".fa-star");
  const tbl1 = $("#tbl-dir");
  const tbl2 = $("#tbl-com");
  const tbl3 = $("#tbl-addcom");
  const tbl4 = $("#tbl-vid");
  const tbl5 = $("#tbl-addrat");
 

  const removeclass = function(e) {
    if (e.hasClass("hide")) e.removeClass("hide");
  };

  const addclass = function(e) {
    if (!e.hasClass("hide")) e.addClass("hide");
  };

  const act1 = function() {
    removeclass(tbl1);
    addclass(tbl2);
    addclass(tbl3);
    addclass(tbl4);
    addclass(tbl5);
  };

  const act2 = function() {
    removeclass(tbl2);
    addclass(tbl1);
    addclass(tbl3);
    addclass(tbl4);
    addclass(tbl5);
  };

  const act3 = function() {
    removeclass(tbl2);
    removeclass(tbl3);
    addclass(tbl1);
    addclass(tbl4);
    addclass(tbl5);
  };

  const act4 = function() {
    removeclass(tbl4);
    addclass(tbl1);
    addclass(tbl2);
    addclass(tbl3);
    addclass(tbl5);
  };

  const act5 = function() {
    removeclass(tbl5);
    addclass(tbl1);
    addclass(tbl2);
    addclass(tbl3);
    addclass(tbl4);
  };

  btn1.on("click", act1);
  btn2.on("click", act2);
  btn3.on("click", act3);
  btn4.on("click", act4);
  btn5.on("click", act5);
});




const btnNextStep = document.getElementById('btn-ns');
const circles = document.querySelectorAll('.circle');
let currentStepIndex = 0;

btnNextStep.addEventListener('click', () => {
  if (currentStepIndex < circles.length) {
    circles[currentStepIndex].classList.add('green');
  }
  currentStepIndex++;
});


const btnAdd = document.querySelector('.btn-add');
const btnSubtract = document.querySelector('.btn-subtract');
const ingredientElements = document.querySelectorAll('[id^=ingredient-]');
const ingQOriginal = [];
const counter = document.querySelector("#counter");;
let portions = 1;

function setCounter(){
  counter.textContent = portions;
}

function getIngQuantities() {
  for (let i = 0; i < ingredientElements.length; i++) {
    const ingredientElement = ingredientElements[i];
    ingQOriginal[i] = parseFloat(ingredientElement.textContent.split('->')[0].trim(), 10);
  }
}
getIngQuantities();

btnAdd.addEventListener('click', () => {
  updateIngredientQuantities(1);
  portions ++;
  setCounter();
});

btnSubtract.addEventListener('click', () => {
  updateIngredientQuantities(-1);
  if(portions>=0){
    portions --;
    setCounter();
    }
});

function updateIngredientQuantities(value) {
  for (let i = 0; i < ingredientElements.length; i++) {
    const ingredientElement = ingredientElements[i];
    const atualQuantity = parseFloat(ingredientElement.textContent.split('->')[0].trim(), 10);
    const newQuantity = atualQuantity + value*ingQOriginal[i];
    if(newQuantity>=0){
    ingredientElement.textContent = `${newQuantity} -> ${ingredientElement.textContent.split('->')[1].trim()}`;
    }
  }
}