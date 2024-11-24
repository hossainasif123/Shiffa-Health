document.addEventListener("DOMContentLoaded", () => {
    const stars = document.querySelectorAll("#star-rating .star");
    let currentRating = 0;
  
    // Function to update stars display
    const updateStars = (rating) => {
      stars.forEach((star, index) => {
        if (index < rating) {
          star.classList.add("filled");
        } else {
          star.classList.remove("filled");
        }
      });
    };
  
    // Add click event listeners to each star
    stars.forEach((star, index) => {
      star.addEventListener("click", () => {
        currentRating = index + 1; // Update current rating
        updateStars(currentRating); // Update stars display
        document.getElementById(`star${currentRating}`).checked = true; // Check the corresponding radio button
      });
    });
  
    // Initialize stars based on pre-selected rating
    const checkedInput = document.querySelector("input[name='rating']:checked");
    if (checkedInput) {
      currentRating = parseInt(checkedInput.value, 10);
      updateStars(currentRating);
    }
  });
  