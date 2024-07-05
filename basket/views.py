from django.shortcuts import render, redirect, reverse, get_object_or_404


import decimal


def view_basket(request):
    """ A view that renders the basket content page """

    
    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the shopping basket """

    product = get_object_or_404(Product, pk=product_id)
    quantity_label = request.POST.get('quantity')
    num_units = int(request.POST.get('num_units', 1))
    redirect_url = request.POST.get('redirect_url')

    if product.has_multiple_sizes:
        quantity_to_kg = {
            '100g': 0.1,
            '250g': 0.25,
            '1kg': 1,
        }

        if quantity_label not in quantity_to_kg:
            return redirect(redirect_url)

        quantity_in_kg = quantity_to_kg[quantity_label]
        total_price = round(product.price * decimal.Decimal(quantity_in_kg) * num_units, 2)

    else:
        quantity_in_kg = 1
        total_price = product.fixed_size_price * num_units

    basket = request.session.get('basket', {})
    item_key = f"{product_id}-{quantity_label}"

    if item_key in basket:
        basket[item_key]['quantity'] += num_units
    else:
        basket[item_key] = {
            'product_id': product.id,
            'quantity_label': quantity_label,
            'quantity_in_kg': quantity_in_kg,
            'price_per_kg': str(product.price if product.has_multiple_sizes else ''),
            'total_price': str(total_price),
            'quantity': num_units,
        }

    request.session['basket'] = basket
    return redirect(redirect_url)
