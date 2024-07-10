from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from products.models import Product
from decimal import Decimal


def view_basket(request):
    """ A view that renders the basket content page """

    
    return render(request, 'basket/basket.html')


def add_to_basket(request, item_id):
    """ Add a quantity of the specified product to the shopping basket """

    product = get_object_or_404(Product, pk=item_id)
    size = request.POST.get('size')
    quantity = int(request.POST.get('quantity', 1))
    redirect_url = request.POST.get('redirect_url', '/')

    basket = request.session.get('basket', {})

    item_key = f"{item_id}-{size}" if size else str(item_id)

    if item_key in basket:
        basket[item_key]['quantity'] += quantity
    else:
        basket[item_key] = {
            'product_id': product.id,
            'size': size,
            'quantity': quantity,
        }

    request.session['basket'] = basket
    return redirect(redirect_url)


def adjust_basket(request, item_id):
    """ Adjust the quantity of a specified product in the shopping basket """

    try:
        item_id = int(item_id)
    except ValueError:
        return HttpResponseBadRequest('Invalid product ID.')

    product = get_object_or_404(Product, pk=item_id)

    size = request.POST.get('size')
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        return HttpResponseBadRequest('Invalid quantity.')

    basket = request.session.get('basket', {})

    item_key = f"{item_id}-{size}" if size else str(item_id)

    if quantity > 0:
        basket[item_key]['quantity'] = quantity

    request.session['basket'] = basket

    basket_total = Decimal('0.00')
    product_count = 0

    for item_key, item_data in basket.items():
        product = get_object_or_404(Product, pk=item_data['product_id'])
        quantity = item_data['quantity']
        size = item_data.get('size', '')

        if product.has_multiple_sizes and size:
            price_for_size = product.get_price_for_size(size)
            if price_for_size is not None:
                product_total = price_for_size * quantity
            else:
                product_total = Decimal('0.00')
        else:
            product_total = (product.fixed_size_price * quantity
                             if product.fixed_size_price else product.price * quantity)

        basket_total += product_total
        product_count += quantity

    
    if basket_total < settings.FREE_SHIPPING_THRESHOLD and basket_total > Decimal('0.00'):
        shipping = (basket_total * Decimal(settings.STANDARD_SHIPPING_PERCENTAGE) / Decimal('100')).quantize(Decimal('0.01'))
        free_shipping_delta = (settings.FREE_SHIPPING_THRESHOLD - basket_total).quantize(Decimal('0.01'))
    else:
        shipping = Decimal('0.00')
        free_shipping_delta = Decimal('0.00')

    grand_total = basket_total + shipping

   
    request.session['total'] = str(basket_total)
    request.session['shipping'] = str(shipping)
    request.session['free_shipping_delta'] = str(free_shipping_delta)
    request.session['grand_total'] = str(grand_total)

   
    return redirect('view_basket')