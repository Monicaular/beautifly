from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.conf import settings
from basket.contexts import basket_contents
from .forms import OrderForm

import stripe

def checkout(request):
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There's nothing in your basket at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()

    # Retrieve basket items and calculate total quantity
    basket_items = basket_contents(request)['basket_items']
    total_quantity = sum(item['quantity'] for item in basket_items)

    # Calculate Stripe total amount (in cents) and create PaymentIntent
    total_amount = int(basket_contents(request)['grand_total'] * 100)
    stripe_total = int(total_amount * 100)
    stripe.api_key = stripe_secret_key
    intent = stripe.PaymentIntent.create(
        amount=stripe_total,
        currency=settings.STRIPE_CURRENCY,
    )

    if not stripe_public_key:
        messages.warning(request, 'Stripe public key is missing. \
            Did you forget to set it in your environment?')
    
    context = {
        'basket_items': basket_items,
        'total': basket_contents(request)['total'],
        'shipping': basket_contents(request)['shipping'],
        'grand_total': basket_contents(request)['grand_total'],
        'order_form': order_form,
        'total_quantity': total_quantity,
        'stripe_public_key': stripe_public_key,
        'client_secret': intent.client_secret,
    }

    return render(request, 'checkout/checkout.html', context)
