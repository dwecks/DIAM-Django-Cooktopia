const btn1 = document.querySelector("#btn-dir");
const btn2 = document.querySelector("#btn-com");
const btn3 = document.querySelector("#btn-addcom");
const tbl1 = document.querySelector("#tbl-dir");
const tbl2 = document.querySelector("#tbl-com");
const tbl3 = document.querySelector("#tbl-addcom");

const removeclass = function (e) {
  if (e.classList.contains("hide")) e.classList.remove("hide");
};

const addclass = function (e) {
  if (!e.classList.contains("hide")) e.classList.add("hide");
};

const act1 = function () {
  removeclass(tbl1);
  addclass(tbl2);
  addclass(tbl3);
};

const act2 = function () {
  removeclass(tbl2);
  addclass(tbl1);
  addclass(tbl3);
};

const act3 = function () {
  removeclass(tbl2);
  removeclass(tbl3)
  addclass(tbl1);
};

btn1.addEventListener("click", act1);
btn2.addEventListener("click", act2);
btn3.addEventListener("click", act3);