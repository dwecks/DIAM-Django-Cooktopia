'use strick'
banners = document.querySelectorAll('.profile-card-flag');


const flagHTML = function (data) {
    console.log(data.flags.png);
    return ` <img class="country-img" src="${data.flags.png}" />`;
  };

  const renderFlag = function(name, element) {
    fetch(`https://restcountries.com/v3.1/name/${name}`)
      .then(function(response) {
        return response.json();
      })
      .then(function(data) {
        try {
          element.innerHTML = flagHTML(data[0]);
          element.classList.remove('hide');
        } catch (error) {
        }
      });
  };

if (banners.length > 0){
    banners.forEach(function(element) {
        renderFlag(element.innerHTML, element);
      });
}