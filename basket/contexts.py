from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404
from products.models import Product


def basket_contents(request):
    """Calculate and return the contents of the shopping basket.

    This function retrieves the current basket from the user's session
    and calculates the total cost, the number of products in the basket,
    and the shipping cost. If the total is below the free shipping threshold,
    it calculates how much more needs to be added to the basket to qualify
    for free shipping.
    Finally, it returns these calculations in a context dictionary that
    can be used in templates.

    Args:
        request: The HTTP request object containing the session data.

    Returns:
        A context dictionary containing:
        - basket_items: A list of dictionaries, each containing item ID,
        quantity, product details, and subtotal.
        - total: The total cost of the products in the basket.
        - product_count: The total number of items in the basket.
        - shipping: The calculated shipping cost
        (or 0 if free shipping applies).
        - free_shipping_delta: The amount required to reach
        the free shipping threshold.
        - free_shipping_threshold: The minimum total required
        for free shipping.
        - grand_total: The total cost including shipping.
    """
    basket_items = []
    total = 0
    product_count = 0
    basket = request.session.get("basket", {})

    for item_id, quantity in basket.items():
        product = get_object_or_404(Product, pk=item_id)
        subtotal = quantity * product.price
        total += subtotal
        product_count += quantity
        basket_items.append(
            {
                "item_id": item_id,
                "quantity": quantity,
                "product": product,
                "subtotal": subtotal,
            }
        )

    if total < settings.FREE_SHIPPING_THRESHOLD:
        shipping = total * Decimal(
            settings.STANDARD_SHIPPING_PERCENTAGE / 100
        )
        free_shipping_delta = settings.FREE_SHIPPING_THRESHOLD - total
    else:
        shipping = 0
        free_shipping_delta = 0

    grand_total = shipping + total

    context = {
        "basket_items": basket_items,
        "total": total,
        "product_count": product_count,
        "shipping": shipping,
        "free_shipping_delta": free_shipping_delta,
        "free_shipping_threshold": settings.FREE_SHIPPING_THRESHOLD,
        "grand_total": grand_total,
    }

    return context
