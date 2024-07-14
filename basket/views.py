from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from products.models import Product
from decimal import Decimal


def view_basket(request):
    """ A view that renders the basket content page """

    
    return render(request, 'basket/basket.html')

def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the shopping basket """

    product = Product.objects.get(pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    basket = request.session.get('basket', {})

    if item_id in list(basket.keys()):
        basket[item_id] += quantity
    else:
        basket[item_id] = quantity

    request.session['basket'] = basket
    messages.success(request, f'Added {quantity} x {product.name} to your basket')

    return redirect(redirect_url)

from django.shortcuts import redirect, reverse

def adjust_basket(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    quantity = int(request.POST.get('quantity'))
    basket = request.session.get('basket', {})

    if quantity > 0:
        basket[item_id] = quantity
    else:
        basket.pop(item_id, None)
        messages.success(request, 'Item removed from your basket')

    request.session['basket'] = basket
    return redirect(reverse('view_basket'))

def remove_from_basket(request, item_id):
    """Remove the item from the shopping basket"""

    try:
        basket = request.session.get('basket', {})

        if str(item_id) in basket:
            del basket[str(item_id)]
            request.session['basket'] = basket
            messages.success(request, 'Item removed successfully from basket.')
        else:
            messages.error(request, 'Item not found in basket.')

    except Exception as e:
        messages.error(request, f'Error removing item from basket: {str(e)}')

    return redirect(reverse('view_basket'))