document.addEventListener('DOMContentLoaded', () => {
    // Define constants for toast elements
    const successToastEl = document.getElementById('successToast');
    const warningToastEl = document.getElementById('warningToast');
    const infoToastEl = document.getElementById('infoToast');
    const errorToastEl = document.getElementById('errorToast');

    // Initialize Bootstrap Toast instances
    const successToast = new bootstrap.Toast(successToastEl);
    const warningToast = new bootstrap.Toast(warningToastEl);
    const infoToast = new bootstrap.Toast(infoToastEl);
    const errorToast = new bootstrap.Toast(errorToastEl);

    
    // Function to show success toast
    const showSuccessToast = () => {
       
        successToast.show();
    };

    // Function to show warning toast
    const showWarningToast = () => {
        warningToast.show();
    };

    // Function to show info toast
    const showInfoToast = () => {
        infoToast.show();
    };

    // Function to show error toast
    const showErrorToast = () => {
        
        errorToast.show();
    };

    



});