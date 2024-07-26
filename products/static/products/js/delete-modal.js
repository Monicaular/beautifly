document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('.delete-product-btn');
  const confirmDeleteButton = document.getElementById('confirm-delete');

  deleteButtons.forEach(button => {
      button.addEventListener('click', (event) => {
          event.preventDefault();
          const productId = event.currentTarget.getAttribute('data-id');
          const deleteUrl = `/products/delete/${productId}/`; // Adjust this URL to match your routing
          confirmDeleteButton.setAttribute('href', deleteUrl);
      });
  });
});