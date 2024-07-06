from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def basket_contents(request):
    basket = request.session.get('basket', {})
    basket_items = []
    total = 0
    product_count = 0
    
    for item_id, item_data in basket.items():
        product = Product.objects.get(pk=item_data['product_id'])
        num_units = item_data['quantity']
        size = item_data.get('size', '')
        if product.has_multiple_sizes:
            price_for_size = product.get_price_for_quantity(size)
            total_price = price_for_size * num_units if price_for_size is not None else 0
        else:
            total_price = product.fixed_size_price * num_units if product.fixed_size_price else product.price * num_units


    total += total_price
    product_count += num_units

    basket_items.append({
            'item_id': item_id,
            'num_units': num_units,
            'product': product,
            'total_price': total_price,
            'size': size,
        })
    if total < settings.FREE_SHIPPING_THRESHOLD:
        shipping = total * Decimal(settings.STANDARD_SHIPPING_PERCENTAGE)
        free_shipping_delta = settings.FREE_SHIPPING_THRESHOLD - total
    else: 
        shipping = 0
        free_shipping_delta = 0
    
    grand_total = shipping + total


    context = {
        'basket_items': basket_items,
        'total': total,
        'product_count': product_count,
        'shipping': shipping,
        'free_shipping_delta': free_shipping_delta,
        'free_shipping_threshold': settings.FREE_SHIPPING_THRESHOLD,
        'grand_total': grand_total,
    }

    return context