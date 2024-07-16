from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from basket.contexts import basket_contents
from .forms import OrderForm

def checkout(request):
    basket = request.session.get('basket', {})
    if not basket:
        messages.error(request, "There's nothing in your basket at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()

    basket_items = basket_contents(request)['basket_items']
    
    total_quantity = sum(item['quantity'] for item in basket_items)
    
    context = {
        'basket_items': basket_items,
        'total': basket_contents(request)['total'],
        'shipping': basket_contents(request)['shipping'],
        'grand_total': basket_contents(request)['grand_total'],
        'order_form': order_form,
        'total_quantity': total_quantity,
        'stripe_public_key': 'pk_test_51L7g7u2QlfePk4wlJYKjg6GUDBCFWIliokOfQYuqsh8YQTSxdfkerRXsCousl50sV8LT4piXLajpy63c5I3GVzB200uyEgU1PC',
        'client_secret': 'test client secret',
    }

    return render(request, 'checkout/checkout.html', context)
