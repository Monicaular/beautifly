from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Wishlist
from products.models import Product

@login_required
def view_wishlist(request):
    """ A view that renders the wishlist content page """

    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')

    context = {
        'wishlist_items': wishlist_items,
    }

    return render(request, 'wishlist/wishlist.html', context)


@login_required
def add_to_wishlist(request, product_id):
    """ Add a product to the user's wishlist """
    product = get_object_or_404(Product, pk=product_id)
    wishlist, created = Wishlist.objects.get_or_create(user=request.user, product=product)

    if created:
        messages.success(request, f'{product.name} has been added to your wishlist.')
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')

    return redirect(request.META.get('HTTP_REFERER', 'products'))

@login_required
def remove_from_wishlist(request, product_id):
    """Remove a product from the user's wishlist"""
    try:
        wishlist_item = get_object_or_404(Wishlist, product_id=product_id, user=request.user)
        wishlist_item.delete()
        messages.success(request, f'{product.name} Item removed from your wishlist.')
    except Wishlist.DoesNotExist:
        messages.error(request, 'Item was not found in your wishlist.')

    return redirect('view_wishlist')