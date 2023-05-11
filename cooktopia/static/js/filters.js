'use stricks'

///////////////////////////////////////////////////////////////
// Select elements
///////////////////////////////////////////////////////////////

const applyBtn = document.querySelector(".applyFiltersButton");
const counter = document.querySelector("#counter");
const search = document.querySelector("#search");
const searchBtn = document.querySelector("#search-btn");

///////////////////////////////////////////////////////////////
// variables
///////////////////////////////////////////////////////////////

let page = 1;
let pageSize = 6;
let selectedRecipes; 

///////////////////////////////////////////////////////////////
// get recipe info from api
///////////////////////////////////////////////////////////////

let recipes;    

fetch('http://127.0.0.1:8000/api/recipes/')
  .then(response => response.json())
  .then(data => {;
    recipes = data;
    selectedRecipes = data; 
    counter.textContent = data.length;
    populateRecipes(data)
    console.log('Recieved recipes:',data)
  })
  .catch(error => console.error('Error:', error));

///////////////////////////////////////////////////////////////
// Filter recipes
///////////////////////////////////////////////////////////////

const searchFunc = function(){
  let filteredRecipes = recipes;

  const difficultyValues = getSelectedCheckboxValues('difficulty');
  if(difficultyValues.length != 0)
    filteredRecipes = filterDifficulty(filteredRecipes, difficultyValues);

  const preparationTimeValues = getSelectedCheckboxValues('preparationTime');
   if(preparationTimeValues.length != 0)
     filteredRecipes = filterPrepTime(filteredRecipes, preparationTimeValues);

  const mealTypeValues = getSelectedCheckboxValues('mealType');
  if(mealTypeValues.length != 0)
    filteredRecipes = filterMeal(filteredRecipes, mealTypeValues);

  const pubDateValue = getSelectedCheckboxValues('pub_date');
  if(pubDateValue.length != 0)
    filteredRecipes = filterPubDate(filteredRecipes, pubDateValue);
 
  const searchText = search.value;
  console.log(searchText);
  if(searchText.length != 0)
    filteredRecipes = filterText(filteredRecipes, searchText);

  selectedRecipes = filteredRecipes

  populateRecipes(filteredRecipes) 
  counter.textContent = filteredRecipes.length;
}

applyBtn.addEventListener("click", searchFunc);
searchBtn.addEventListener("click", searchFunc);

///////////////////////////////////////////////////////////////
// Pages
///////////////////////////////////////////////////////////////

// Page size
$(document).ready(function() {
  // Select the select dropdown element
  const $selectPage = $('#select-page');

  // Define an event handler for the change event
  $selectPage.on('change', function() {
    // Update the pageSize variable with the selected value
    pageSize = parseInt($(this).val());
    console.log('Selected page size:', pageSize);
    
    // Call the function to repopulate the recipes with the new pageSize
    populateRecipes(selectedRecipes);
  });
});

// Page selector
function createPageSelector(n) {
  const $pagesContainer = $('.page-selector');
  const ul = $("<ul>");

  for (let i = 1; i <= n; i++) {
    const li = $("<li>")
      .addClass("p2-r")
      .text("Page " + i)
      .data("page", i); // Add data attribute with the page value
    ul.append(li);
  }

  $pagesContainer.append(ul);

  // Attach click event handler to handle page selection
  ul.on("click", "li", function() {
    const nextPage = $(this).data("page");
    console.log("Selected page:", page);

    page = nextPage
    populateRecipes(selectedRecipes);
  });
}

$(document).ready(function() {
  createPageSelector(5);
});

///////////////////////////////////////////////////////////////
// Help Functions
///////////////////////////////////////////////////////////////

// Get checked checkboxes
  function getSelectedCheckboxValues(name) {
    const checkboxes = $('input[name="' + name + '"]:checked');
    const values = [];
    checkboxes.each(function() {
      values.push($(this).val());
    });
    console.log('Selected ' + name + ' values:', values);
    return values;
  }

///////////////////////////////////////////////////////////////
// Help Filters
///////////////////////////////////////////////////////////////

  function filterDifficulty(recipes, filters) {
    //console.log(filters);
    return recipes.filter(recipe => {
      // Check if the chef matches the difficulty filter
      for (const value of filters)
        if(recipe.difficulty == value)
          return recipe;
    });
  }

  function filterPrepTime(recipes, filters) {
    const prepTimes = [[0, 30], [30, 60], [60, 120]];
    return recipes.filter(recipe => {
      // Check if the chef matches the difficulty filter
      for (const value of filters)
        if(parseInt(recipe.preparationTime) >= prepTimes[value][0] &&  parseInt(recipe.preparationTime) <= prepTimes[value][1])
          return recipe;
    });
  }


  function filterMeal(recipes, filters) {
    return recipes.filter(recipe => {
      // Check if the chef matches the difficulty filter
      for (const value of filters)
        if(recipe.mealType == value)
          return recipe;
    });
  }

  
function filterPubDate(recipes, filters) {
  return recipes.filter(recipe => {
    for (const value of filters) {
      const currentDate = new Date();
      const pubDate = new Date(recipe.pub_date);

      if (value === 'week') {
        const oneWeekAgo = new Date(currentDate.getTime() - 7 * 24 * 60 * 60 * 1000);
        if (pubDate >= oneWeekAgo && pubDate <= currentDate) {
          return recipe;
        }
      } else if (value === 'month') {
        const oneMonthAgo = new Date(currentDate.getFullYear(), currentDate.getMonth() - 1, currentDate.getDate());
        if (pubDate >= oneMonthAgo && pubDate <= currentDate) {
          return recipe;
        }
      } else if (value === 'year') {
        const oneYearAgo = new Date(currentDate.getFullYear() - 1, currentDate.getMonth(), currentDate.getDate());
        if (pubDate >= oneYearAgo && pubDate <= currentDate) {
          return recipe;
        }
      }
    }
  });
}

function filterText(recipes, searchText) {
  const keywords = searchText.toLowerCase().split(" ").filter(word => word.length > 2);
  return recipes.filter(recipe => {
    // Check if the chef matches the difficulty filter
    for (const keyword of keywords)
      if(recipe.title.toLowerCase().includes(keyword))
        return recipe;
  });
}

///////////////////////////////////////////////////////////////
// Html generators
///////////////////////////////////////////////////////////////

// Populates recipes container
function populateRecipes(recipes) {
  const $recipesContainer = $('#recipes');
  // Clear the existing content
  $recipesContainer.empty();

  // Calculate the start and end index of the selected recipes based on the page and page size
  const startIndex = (page - 1) * pageSize;
  const endIndex = startIndex + pageSize;
  // Get the selected recipes as a sub-array
  const pageRecipes = recipes.slice(startIndex, endIndex);

  // Create a recipe card for each recipe and append it to the container
  pageRecipes.forEach(function(recipe) {
    const $recipeCard = createRecipeCard(recipe);
    $recipesContainer.append($recipeCard);
  });
}

// basic recipe card
function createRecipeCard(recipe) {
  const card = document.createElement("div");
  card.classList.add("basic-card", "N000-b");
  const imgBox = document.createElement("picture");
  imgBox.classList.add("basic-card-imgbox");
  const img = document.createElement("img");
  img.setAttribute("src", recipe.image);
  img.setAttribute("alt", "Recipe Image");
  imgBox.appendChild(img);
  card.appendChild(imgBox);
  const content = document.createElement("div");
  content.classList.add("basic-card-content", "flex-c");
  const titleBox = document.createElement("div");
  const title = document.createElement("h3");
  title.classList.add("h4");
  title.textContent = recipe.title;
  const chef = document.createElement("h4");
  chef.classList.add("p1-b", "N700-c");
  chef.textContent = "By Chef";
  titleBox.appendChild(title);
  titleBox.appendChild(chef);
  content.appendChild(titleBox);
  const desc = document.createElement("p");
  desc.classList.add("p1-r", "basic-card-hiden");
  desc.textContent = recipe.description;
  const exploreBtn = document.createElement("a");
  exploreBtn.classList.add("btn-swipe", "l1-r", "basic-card-hiden");
  exploreBtn.textContent = "Explore Recipe";
  exploreBtn.setAttribute("href", `http://127.0.0.1:8000/recipes/${recipe.id}/`);
  content.appendChild(desc);
  content.appendChild(exploreBtn);
  card.appendChild(content);
  return card;
}
