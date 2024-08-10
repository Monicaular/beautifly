from django.shortcuts import render, get_object_or_404, redirect
from .models import UserProfile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from checkout.models import Order
from wishlist.models import Wishlist


@login_required
def profile(request):
    """
    Display and allow updating of the user's profile.
    """

    profile = get_object_or_404(UserProfile, user=request.user)
    wishlist_items = Wishlist.objects.filter(user=request.user)

    if request.method == "POST":
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
            return redirect("profile")
    else:
        form = UserProfileForm(instance=profile)

    orders = profile.orders.all()

    template = "profiles/profile.html"
    context = {
        "form": form,
        "orders": orders,
        "profile": profile,
        "wishlist_items": wishlist_items,
        "on_profile_page": True,
    }

    return render(request, template, context)


@login_required
def order_history(request, order_number):
    """
    Display the details of a past order from the user's order history.
    """
    order = get_object_or_404(Order, order_number=order_number)
    lineitems = order.lineitems.all()

    messages.info(
        request,
        (
            f"This is a past confirmation for order number {order_number}. "
            "A confirmation email was sent on the order date."
        ),
    )

    template = "checkout/checkout_success.html"
    context = {
        "order": order,
        "lineitems": lineitems,
        "from_profile": True,
    }

    return render(request, template, context)
