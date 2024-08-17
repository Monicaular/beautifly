# Testing

Return back to the [README.md](README.md) file.

Throughout the development of this project, I carried out extensive testing to verify that every aspect of the website operates as intended. This section provides comprehensive documentation of all the tests conducted, detailing the procedures, outcomes, and any issues identified and resolved. Each test was designed to rigorously assess the functionality, performance, and user experience of the site, ensuring that it meets the highest standards of quality and reliability.


## Code Validation

I thoroughly tested all of my code using the recommended programming tools for each specific language.

### HTML

I utilized the [W3C HTML Validator](https://validator.w3.org), the recommended tool, to thoroughly validate all of my HTML files.

| Page            | W3C URL                                                                                                                                                   | Screenshot                                 | Notes            |
| --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------ | ---------------- |
| Home            | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2F)                                                             | ![screenshot](/documentation/homepage-html-validation.png)  | Pass: No Errors  |
| All Products Page           | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fproducts%2F)                                                             | ![screenshot](/documentation/products-html-validation.png)  | Pass: No Errors  |
| Product Detail           | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fproducts%2F)                                                             | ![screenshot](/documentation/product-detail-html-validation.png)  | Pass: No Errors  |
| About US           | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fabout%2F)                                                             | ![screenshot](/documentation/about-us-html-validation.png)  | Pass: No Errors  |
| Privacy Policy          | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fprivacy-policy%2F)                                                             | ![screenshot](/documentation/privacy-policy-html-validation.png)  | Pass: No Errors  |
| Delivery Info           | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fdelivery-terms%2F)                                                             | ![screenshot](/documentation/delivery-terms-html-validation.png)  | Pass: No Errors  |
| Returns Policy           | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fquality_guarantee%2F)                                                             | ![screenshot](/documentation/returns-policy-html-validation.png)  | Pass: No Errors  |
| Account Info          | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fprofile%2F)                                                             | ![screenshot](/documentation/account-info-html-validation.png)  | Pass: No Errors  |
| Log Out          | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Faccounts%2Flogout%2F)                                                             | ![screenshot](/documentation/log-out-html-validation.png)  | Pass: No Errors  |
| Log In          | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Faccounts%2Flogin%2F)                                                             | ![screenshot](/documentation/log-in-html-validation.png)  | Pass: No Errors  |
| Register         | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Faccounts%2Flogin%2F)                                                             | ![screenshot](/documentation/register-html-validation.png)  | Pass: No Errors  |
| Add Product        | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Faccounts%2Flogin%2F)                                                             | ![screenshot](/documentation/add-product-html-validation.png)  | Pass: No Errors  |
| Edit Product        | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fproducts%2Fedit%2F86%2F)                                                             | ![screenshot](/documentation/edit-product-html-validation.png)  | Pass: No Errors  |
| Basket        | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fbasket%2F)                                                             | ![screenshot](/documentation/basket-html-validation.png)  | Pass: No Errors  |
| Checkout        | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fcheckout%2F)                                                             | ![screenshot](/documentation/checkout-html-validation.png)  | Pass: No Errors  |
|Checkout Success        | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fbasket%2F)                                                             | ![screenshot](/documentation/checkout-success-html-validation.png)  | Pass: No Errors  |
|Wishlist        | [W3C](https://validator.w3.org/nu/?doc=https%3A%2F%2Fwholesome-basket-e-commerce-72c9883373ee.herokuapp.com%2Fwishlist%2F)                                                             | ![screenshot](/documentation/wishlist-html-validation.png)  | Pass: No Errors  |

### CSS Validation

I have validated all of my CSS files using the [W3C CSS Validator](https://jigsaw.w3.org/css-validator).

| File           | Screenshot                                                    | Notes            |
|----------------|---------------------------------------------------------------|------------------|
| `base.css`     | ![Screenshot](documentation/base-css-validation.png)          | Pass: No Errors  |
| `checkout.css` | ![Screenshot](documentation/checkout-css-validation.png)      | Pass: No Errors  |
| `profile.css`  | ![Screenshot](documentation/profiles-css-validation.png)      | Pass: No Errors  |


### JavaScript Validation

I have validated all of my JS files using the [JSHint Validator](https://jshint.com).

| File                                | Screenshot                                          | Notes                                               |
|-------------------------------------|----------------------------------------------------|-----------------------------------------------------|
| `basket.html` (postloadjs)            | ![Screenshot](documentation/basket-html-js-code.png)         | Pass: No Errors                                     |
| `stripe_elements.js`                  | ![Screenshot](documentation/stripe_elements-js.png)         | Pass: No Errors                                     |
| `delete_modal.js`     | ![Screenshot](documentation/delete_modal_js.png)         | Pass: No Errors                                     |
| `preview-product-image.js`    | ![Screenshot](documentation/preview-product-image.png)         | Pass: No Errors                                     |
| `rating.js`       | ![Screenshot](documentation/rating-js.png)         | Pass: No Errors                                     |
| `adjust-quantity-script.html`             | ![Screenshot](documentation/adjust-quantity-script-html.png)         | Pass: No Errors                                     |
| `products-categories-display-script.html`        | ![Screenshot](documentation/products-category-display-html.png)         | Pass: No Errors |
| `add_product.html` (postloadjs)                | ![Screenshot](documentation/add-product-postload-js.png)          | Pass: No Errors                           |
| `edit_product.html` (postloadjs)                | ![Screenshot](documentation/edit-product-postload-js.png)          | Pass: No Errors                           |
| `toasts.js`               | ![Screenshot](documentation/edit-product-postload-js.png)          | Unused variables: 	showSuccessToast, showWarningToast, showInfoToast, showErrorToast |
| `base.html` (postloadjs)                | ![Screenshot](documentation/base-html-postloads.png)          | Pass: No Errors                           |













