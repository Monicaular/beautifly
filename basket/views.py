from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.conf import settings
from products.models import Product
from decimal import Decimal


def view_basket(request):
    """ A view that renders the basket content page """

    
    return render(request, 'basket/basket.html')


