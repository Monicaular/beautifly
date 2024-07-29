document.addEventListener('DOMContentLoaded', () => {
  const deleteButtons = document.querySelectorAll('.delete-btn');
  const confirmDeleteButton = document.getElementById('confirm-delete');

  deleteButtons.forEach(button => {
      button.addEventListener('click', (event) => {
          event.preventDefault();
          const productId = event.currentTarget.getAttribute('data-id');
          const deleteUrl = `/products/delete/${productId}/`;
          confirmDeleteButton.setAttribute('href', deleteUrl);
      });
  });
});