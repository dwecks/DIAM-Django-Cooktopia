'use stricks'

let recipes;

fetch('http://127.0.0.1:8000/api/recipes/')
  .then(response => response.json())
  .then(data => {;
    recipes = data;
    console.log(data);
    console.log("GGGGGGGGGGGGGGGGF");
    populateRecipes(data)
    console.log("FFFFFFFFFFFFFFFFFFFFFFFFFF");
  })
  .catch(error => console.error('Error:', error));

  const btn = document.querySelector(".applyFiltersButton");

  btn.addEventListener("click", () => {
    console.log(recipes);

    const difficultyValues = getSelectedCheckboxValues('difficulty');
    console.log("FFFFFFFFFFFFFFFFFFFFFFFFFF");
    console.log(filterRecipes(recipes, difficultyValues));
    
  });



  function getSelectedCheckboxValues(name) {
    const checkboxes = $('input[name="' + name + '"]:checked');
    const values = [];
    checkboxes.each(function() {
      values.push($(this).val());
    });
    console.log('Selected ' + name + ' values:', values);
    return values;
  }

  
  function filterRecipes(recipes, filters) {
    //console.log(filters);
    return recipes.filter(recipe => {
      // Check if the chef matches the difficulty filter
      for (const value of filters)
        if(recipe.difficulty == value)
          return recipe;
    });
  }


  // expand filters
  $(document).ready(function() {
    // Select all elements whose ID starts with 'filter-'
    const $filters = $("[id^='filter-']");
    
    // Loop through each filter element
    $filters.each(function() {
        // Get a reference to the filter element
        const $filter = $(this);
        // Extract the ID of the filter element
        const id = $filter.attr("id").replace("filter-", "");
        // Select the corresponding icon and labels elements using template literals
        const $icon = $(`#icon-${id}`);
        const $labels = $(`#labels-${id}`);
        
        // Log the filter element and icon element to the console
        //console.log($filter);
        //console.log($icon);
        
        // Define a function to toggle the classes on the icon and labels elements
        const openFilter = function() {
            $icon.toggleClass("rotate");
            $labels.toggleClass("reduce");
            console.log("click");
        };
        
        // Remove any existing click event listeners on the filter element and bind a new one
        $filter.off("click").on("click", openFilter);
    });
});

  // hide filters
  $(document).ready(function() {
    // Select the filter button element
    const $filterBtn = $("#filter-toggle");
    // Select the element that you want to hide
    const $hideEl = $("#filters");
  
    // Define a function to handle the click event
    const toggleFilters = function() {
      // Toggle the 'hidden' class on the element to hide
      $hideEl.toggleClass("hide");
    };
  
    // Remove any existing click event listeners on the filter button and bind a new one
    $filterBtn.off("click").on("click", toggleFilters);
  });


////////////////////////////////////////////////////////////////////////
function createRecipeCard(recipe) {
  console.log("Olsssssssssssssssssssss");
  const card = document.createElement("div");
  card.classList.add("basic-card", "N000-b");
  console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
  const imgBox = document.createElement("picture");
  imgBox.classList.add("basic-card-imgbox");
  console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
  const img = document.createElement("img");
  console.log("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA");
  img.setAttribute("src", recipe.image.url);
  console.log("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF");
  img.setAttribute("alt", "Recipe Image");
  imgBox.appendChild(img);
  card.appendChild(imgBox);
  console.log("BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB");
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
  console.log("CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC");
  const desc = document.createElement("p");
  desc.classList.add("p1-r", "basic-card-hiden");
  desc.textContent = recipe.description;
  const exploreBtn = document.createElement("a");
  exploreBtn.classList.add("btn-swipe", "l1-r", "basic-card-hiden");
  exploreBtn.textContent = "Explore Recipe";
  exploreBtn.addEventListener("click", function() {
    // Handle click event for Explore Recipe button
    // You can use recipe.id to get the ID of the selected recipe
  });
  content.appendChild(desc);
  content.appendChild(exploreBtn);
  card.appendChild(content);
  console.log("DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD");
  return card;
}

function populateRecipes(recipes) {
  const $recipesContainer = $('#recipes');
console.log("Olaaaaaaaaaaaaaas");
  // Clear the existing content
  $recipesContainer.empty();

  // Create a recipe card for each recipe and append it to the container
  recipes.forEach(function(recipe) {
    const $recipeCard = createRecipeCard(recipe);
    console.log($recipeCard);
    $recipesContainer.append($recipeCard);
  });
}

function applyFilters() {
    console.log("applyFilters() function called");
  // Get the selected filter values
  const difficultyValues = getSelectedCheckboxValues('difficulty');
  const preparationTimeValues = getSelectedCheckboxValues('preparationTime');
  const mealTypeValues = getSelectedCheckboxValues('mealType');
  const pubDateValue = getSelectedCheckboxValues('pub_date');

  // Build the query string for the filter values
  const queryString = `difficulty=${difficultyValues.join(',')}&preparationTime=${preparationTimeValues.join(',')}&mealType=${mealTypeValues.join(',')}&pub_date=${pubDateValue}`;
// Load the filtered recipes into the "receitas_content" <div>
  //$('#recipeContainer').load('/filter_recipes' + queryString);

  // Perform the filtering logic here

  // Hide all recipe cards
  $('.receitas_content .recipeCard').hide();

  // Filter and display the recipe cards based on the selected filter values
  $('.receitas_content .recipeCard').each(function() {
    const difficulty = $(this).data('difficulty');
    const preparationTime = $(this).data('preparationtime');
    const mealType = $(this).data('mealtype');
    const pubDate = $(this).data('pub_date');

    if (
      (difficultyValues.length === 0 || difficultyValues.includes(difficulty)) &&
      (preparationTimeValues.length === 0 || preparationTimeValues.includes(preparationTime)) &&
      (mealTypeValues.length === 0 || mealTypeValues.includes(mealType)) &&
      (pubDateValue === undefined || pubDateValue === pubDate)
    ) {
      $(this).show(); // Display the recipe card
    }
  });
}



