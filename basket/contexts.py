from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product

def basket_contents(request):
    basket = request.session.get('basket', {})
    basket_items = []
    basket_total = Decimal('0.00')
    product_count = 0
    
    for item_key, item_data in basket.items():
        product = get_object_or_404(Product, pk=item_data['product_id'])
        num_units = item_data['quantity']
        size = item_data.get('size', '')

        if product.has_multiple_sizes and size:
            price_for_size = product.get_price_for_quantity(size)
            if price_for_size is not None:
                product_total = price_for_size * num_units
            else:
                product_total = Decimal('0.00')
        else:
            product_total = product.fixed_size_price * num_units if product.fixed_size_price else product.price * num_units


        basket_total += product_total
        product_count += num_units

        basket_items.append({
                'item_id': item_key,
                'num_units': num_units,
                'product': product,
                'total_price': product_total,
                'size': size,
            })
    if basket_total < settings.FREE_SHIPPING_THRESHOLD and basket_total > Decimal('0.00'):
        shipping = (basket_total * Decimal(settings.STANDARD_SHIPPING_PERCENTAGE) / Decimal('100')).quantize(Decimal('0.01'))
        free_shipping_delta = (settings.FREE_SHIPPING_THRESHOLD - basket_total).quantize(Decimal('0.01'))
    else: 
        shipping = Decimal('0.00')
        free_shipping_delta = Decimal('0.00')

    grand_total = basket_total + shipping


    context = {
        'basket_items': basket_items,
        'total': basket_total,
        'product_count': product_count,
        'shipping': shipping,
        'free_shipping_delta': free_shipping_delta,
        'free_shipping_threshold': settings.FREE_SHIPPING_THRESHOLD,
        'grand_total': grand_total,
    }

    return context

