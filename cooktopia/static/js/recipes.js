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