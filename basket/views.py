from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse
from products.models import Product
from decimal import Decimal



def view_basket(request):
    """ A view that renders the basket content page """

    
    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the shopping basket """

    product = get_object_or_404(Product, pk=item_id)
    size = request.POST.get('size')
    num_units = int(request.POST.get('num_units', 1))
    redirect_url = request.POST.get('redirect_url')

    if product.has_multiple_sizes:
        quantity_to_kg = {
            '100g': Decimal('0.1'),
            '250g': Decimal('0.25'),
            '1kg': Decimal('1'),
        }

        if size not in quantity_to_kg:
            return redirect(redirect_url)

        quantity_in_kg = quantity_to_kg[size]
        total_price = round(product.price * Decimal(quantity_in_kg) * num_units, 2)

    else:
        quantity_in_kg = 1
        total_price = product.fixed_size_price * num_units

    basket = request.session.get('basket', {})
    item_id = f"{product_id}-{size}"

    if item_id in basket:
        basket[item_id]['quantity'] += num_units
    else:
        basket[item_id] = {
            'product_id': product.id,
            'size': size,
            'quantity_in_kg': quantity_in_kg,
            'price_per_kg': str(product.price if product.has_multiple_sizes else ''),
            'total_price': str(total_price),
            'quantity': num_units,
        }

    request.session['basket'] = basket
    return redirect(redirect_url)