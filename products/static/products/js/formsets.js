document.addEventListener('DOMContentLoaded', function () {
    function addFormRow(formset, prefix) {
        let formCount = parseInt(document.querySelector(`#id_${prefix}-TOTAL_FORMS`).value);
        let newFormHtml = formset.querySelector('.formset-template').innerHTML.replace(/__prefix__/g, formCount);
        formset.insertAdjacentHTML('beforeend', newFormHtml);
        document.querySelector(`#id_${prefix}-TOTAL_FORMS`).value = formCount + 1;
        updateRemoveButtons();
    }

    function updateRemoveButtons() {
        document.querySelectorAll('.remove-form-row').forEach(btn => {
            btn.removeEventListener('click', removeFormRow);
            btn.addEventListener('click', removeFormRow);
        });
    }

    function removeFormRow(event) {
        event.preventDefault();
        let row = event.target.closest('.formset-row');
        if (row) {
            row.remove();
            updateFormsetIndices();
        }
    }

    function updateFormsetIndices() {
        ['nutritional_facts', 'related_products', 'fast_facts'].forEach(prefix => {
            let forms = document.querySelectorAll(`#${prefix}-formset .formset-row`);
            forms.forEach((form, index) => {
                form.querySelectorAll('input, select, textarea').forEach(input => {
                    let nameRegex = new RegExp(`(${prefix}-\\d+-)`);
                    let newName = `${prefix}-${index}-`;
                    input.name = input.name.replace(nameRegex, newName);
                    input.id = input.id.replace(nameRegex, newName);
                });
            });
            document.querySelector(`#id_${prefix}-TOTAL_FORMS`).value = forms.length;
        });
    }

    document.querySelector('#add-nutrition-fact').addEventListener('click', function () {
        addFormRow(document.querySelector('#nutrition-facts-formset'), 'nutritional_facts');
    });

    document.querySelector('#add-related-product').addEventListener('click', function () {
        addFormRow(document.querySelector('#related-products-formset'), 'related_products');
    });

    document.querySelector('#add-fast-fact').addEventListener('click', function () {
        addFormRow(document.querySelector('#fast-facts-formset'), 'fast_facts');
    });

    updateRemoveButtons();
});