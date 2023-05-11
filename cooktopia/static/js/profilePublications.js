///////////////////////////////////////////////////////////////
// Select elements
///////////////////////////////////////////////////////////////
const profileContent = document.getElementById("profile-content");
const cards = Array.from(profileContent.querySelectorAll(".basic-card"));

///////////////////////////////////////////////////////////////
// Variables
///////////////////////////////////////////////////////////////
let page = 1;
let pageSize = 6;

populateRecipes(cards)
///////////////////////////////////////////////////////////////
// Funções auxiliares
///////////////////////////////////////////////////////////////
// Page selector
function createPageSelector(n) {
    const $pagesContainer = $('.page-selector');
    $pagesContainer.empty();

    // create pages
    const ul = $("<ul>");
    for (let i = 1; i <= n; i++) {
      const li = $("<li>")
        .addClass("p2-r")
        .text("Page " + i)
        .data("page", i); // Add data attribute with the page value
        if(i == page)
          li.addClass("active")
      ul.append(li);
    }
  
    $pagesContainer.append(ul);

    // Attach click event handler to handle page selection
    ul.on("click", "li", function() {
      const nextPage = $(this).data("page");
      console.log("Selected page:", nextPage);
      page = nextPage
      populateRecipes(cards);
    });
  }

// Populates profile
function populateRecipes(cards) {
    const $container = $('#profile-content');
    // Clear the existing content
    $container.empty();
    // Calculate the start and end index of the selected recipes based on the page and page size
    const startIndex = (page - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    // Get the selected recipes as a sub-array
    const pageContent = cards.slice(startIndex, endIndex);
    // Generate page selector
    createPageSelector(Math.ceil(cards.length / pageSize));
    // Create a recipe card for each recipe and append it to the container
    pageContent.forEach(function(card) {
        console.log("AAAAAAAAAAAAAAAAAAAAAAAAA");
        console.log(card);
      $container.append(card);
    });
  }