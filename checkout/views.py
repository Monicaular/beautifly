from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.conf import settings
from basket.contexts import basket_contents
from .models import Order, OrderLineItem
from .forms import OrderForm
from products.models import Product
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from .utils import get_iso_country_code

import stripe
import json


@require_POST
def cache_checkout_data(request):
    """
    Cache checkout data in the PaymentIntent's metadata.
    """
    try:
        pid = request.POST.get("client_secret").split("_secret")[0]

        stripe.api_key = settings.STRIPE_SECRET_KEY

        stripe.PaymentIntent.modify(
            pid,
            metadata={
                "basket": json.dumps(request.session.get("basket", {})),
                "save_info": request.POST.get("save_info"),
                "username": (
                    request.user.username
                    if request.user.is_authenticated
                    else ""
                ),
            },
        )

        return HttpResponse(status=200)
    except Exception as e:
        messages.error(
            request,
            "Sorry, your payment cannot be processed right now. Please try again later.",
        )
        return HttpResponse(content=str(e), status=400)


def checkout(request):
    """
    Handle the checkout process, including order creation and payment.
    """
    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == "POST":
        basket = request.session.get("basket", {})
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get("client_secret").split("_secret")[0]
            print("stripe pid from form POST request", pid, " ****")
            order.stripe_pid = pid
            order.original_basket = json.dumps(basket)
            order.save()

            for item_id, item_data in basket.items():
                try:
                    product = Product.objects.get(id=item_id)
                    order_line_item = OrderLineItem(
                        order=order,
                        product=product,
                        quantity=item_data,
                    )
                    order_line_item.save()
                except Product.DoesNotExist:
                    messages.error(
                        request,
                        (
                            "One of the products in your basket wasn't found in our database."
                        ),
                    )
                    order.delete()
                    return redirect(reverse("view_basket"))

            request.session["save_info"] = "save-info" in request.POST
            return redirect(
                reverse("checkout_success", args=[order.order_number])
            )
        else:
            messages.error(
                request,
                "There was an error with your form. \
                Please double check your information.",
            )
    else:
        basket = request.session.get("basket", {})

        if not basket:
            messages.error(
                request, "There's nothing in your basket at the moment"
            )
            return redirect(reverse("products"))

        current_basket = basket_contents(request)
        stripe_total = int(basket_contents(request)["grand_total"] * 100)
        stripe.api_key = stripe_secret_key
        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order_form = OrderForm(
                    initial={
                        "full_name": profile.user.get_full_name(),
                        "email": profile.user.email,
                        "phone_number": profile.default_phone_number,
                        "country": profile.default_country,
                        "postcode": profile.default_postcode,
                        "town_or_city": profile.default_town_or_city,
                        "street_address1": profile.default_street_address1,
                        "street_address2": profile.default_street_address2,
                        "county": profile.default_county,
                    }
                )
            except UserProfile.DoesNotExist:
                order_form = OrderForm()
        else:
            order_form = OrderForm()

        basket_items = basket_contents(request)["basket_items"]
        total_quantity = sum(item["quantity"] for item in basket_items)

    if not stripe_public_key:
        messages.warning(
            request,
            "Stripe public key is missing. \
            Did you forget to set it in your environment?",
        )

    template = "checkout/checkout.html"

    context = {
        "basket_items": basket_items,
        "total": basket_contents(request)["total"],
        "shipping": basket_contents(request)["shipping"],
        "grand_total": basket_contents(request)["grand_total"],
        "order_form": order_form,
        "total_quantity": total_quantity,
        "stripe_public_key": stripe_public_key,
        "client_secret": intent.client_secret,
    }

    return render(request, "checkout/checkout.html", context)


def checkout_success(request, order_number):
    """
    Handle successful checkouts and update user profile if requested.
    """
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(
        request,
        f"Order successfully processed! \
        Your order number is {order_number}. A confirmation \
        email will be sent to {order.email}.",
    )

    if "basket" in request.session:
        del request.session["basket"]

    save_info = request.session.get("save_info")
    if save_info:
        profile = UserProfile.objects.get(user=request.user)

        order.user_profile = profile
        order.save()

        profile_data = {
            "default_phone_number": order.phone_number,
            "default_country": order.country,
            "default_postcode": order.postcode,
            "default_town_or_city": order.town_or_city,
            "default_street_address1": order.street_address1,
            "default_street_address2": order.street_address2,
            "default_county": order.county,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()
        else:
            messages.error(
                request, "There was an error updating your profile."
            )

    context = {
        "order": order,
    }

    return render(request, "checkout/checkout_success.html", context)
