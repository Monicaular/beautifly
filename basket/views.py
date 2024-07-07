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
    redirect_url = request.POST.get('redirect_url', '/')

    basket = request.session.get('basket', {})

    item_key = f"{item_id}-{size}" if size else str(item_id)

    if item_key in basket:
        basket[item_key]['quantity'] += num_units
    else:
        basket[item_key] = {
            'product_id': product.id,
            'size': size,
            'quantity': num_units,
        }

    request.session['basket'] = basket
    return redirect(redirect_url)