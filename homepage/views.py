from django.shortcuts import render
from .models import CarouselItem


def index(request):
    carousel_items = CarouselItem.objects.filter(is_active=True)
    context = {
        'carousel_items': carousel_items,
    }
    return render(request, 'homepage/index.html', context)
