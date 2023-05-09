

function applyFilters() {
  // Get the selected filter values
  const difficultyValues = getSelectedCheckboxValues('difficulty');
  const preparationTimeValues = getSelectedCheckboxValues('preparationTime');
  const mealTypeValues = getSelectedCheckboxValues('mealType');
  const pubDateValue = getSelectedCheckboxValues('pub_date');

  // Build the query string for the filter values
  const queryString = `difficulty=${difficultyValues.join(',')}&preparationTime=${preparationTimeValues.join(',')}&mealType=${mealTypeValues.join(',')}&pub_date=${pubDateValue}`;
// Load the filtered recipes into the "receitas_content" <div>
  $('#recipeContainer').load('/filter_recipes?' + queryString);

  // Perform the filtering logic here

  // Hide all recipe cards
  /*$('.receitas_content .recipeCard').hide();

  // Filter and display the recipe cards based on the selected filter values
  $('.receitas_content .recipeCard').each(function() {
    const difficulty = $(this).data('difficulty');
    const preparationTime = $(this).data('preparationtime');
    const mealType = $(this).data('mealtype');
    const pubDate = $(this).data('pubdate');

    if (
      (difficultyValues.length === 0 || difficultyValues.includes(difficulty)) &&
      (preparationTimeValues.length === 0 || preparationTimeValues.includes(preparationTime)) &&
      (mealTypeValues.length === 0 || mealTypeValues.includes(mealType)) &&
      (pubDateValue === undefined || pubDateValue === pubDate)
    ) {
      $(this).show(); // Display the recipe card
    }
  });*/
}

function getSelectedCheckboxValues(name) {
  const checkboxes = $('input[name="' + name + '"]:checked');
  const values = [];
  checkboxes.each(function() {
    values.push($(this).val());
  });
  return values;
}