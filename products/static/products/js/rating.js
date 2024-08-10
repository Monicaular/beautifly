document.addEventListener('DOMContentLoaded', function() {
    const rateProductLink = document.getElementById('rate-product-link');
    const ratingFormContainer = document.getElementById('rating-form-container');
    const hearts = document.querySelectorAll('#rating-hearts i');
    const ratingInput = document.getElementById('id_value');
    const cancelRatingButton = document.getElementById('cancel-rating');

    // Show the rating form when the "Rate this product" link is clicked
    rateProductLink.addEventListener('click', function(event) {
        event.preventDefault();
        ratingFormContainer.style.display = 'block';
        rateProductLink.style.display = 'none';
    });

    // Hide the rating form and show the "Rate this product" link again when "Cancel" is clicked
    cancelRatingButton.addEventListener('click', function(event) {
        ratingFormContainer.style.display = 'none';
        rateProductLink.style.display = 'block';
    });

    // Handle heart selection
    hearts.forEach(heart => {
        heart.addEventListener('click', function() {
            const value = this.getAttribute('data-value');
            ratingInput.value = value;  // Set the hidden input's value

            // Update the visual state of the hearts
            hearts.forEach(h => {
                if (h.getAttribute('data-value') <= value) {
                    h.classList.remove('bi-heart');
                    h.classList.add('bi-heart-fill');
                } else {
                    h.classList.remove('bi-heart-fill');
                    h.classList.add('bi-heart');
                }
            });
        });
    });
});