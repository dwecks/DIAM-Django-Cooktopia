console.log("Clara")

let recipes;

fetch('http://127.0.0.1:8000/api/recipes/')
  .then(response => response.json())
  .then(data => {;
    recipes = data;

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



