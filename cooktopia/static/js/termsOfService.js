console.log("hello");

const checkbox = document.querySelector('#terms-checkbox');
const button = document.querySelector('#create-btn');

checkbox.addEventListener('change', function() {
  if (this.checked) {
    button.disabled = false;
  } else {
    button.disabled = true;
  }
});