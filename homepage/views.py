from django.shortcuts import render
from .models import CarouselItem
from products.models import Category


def index(request):
    carousel_items = CarouselItem.objects.filter(is_active=True)
    categories = Category.objects.exclude(name__in=['tofu', 'chilled', 'savoury_snacks', 'sweet_snacks', 'vegan_cheese', 'powders', 'flours_and_powders', 'pantry_staples', 'snacks_and_treats'])

    context = {
        'carousel_items': carousel_items,
        'categories': categories,
    }

    
    return render(request, 'homepage/index.html', context)
