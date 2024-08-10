from django.shortcuts import render, redirect, get_object_or_404
from products.models import Category


def index(request):
    """
    Render the homepage with a list of categories, excluding certain ones.
    """
    categories = Category.objects.exclude(
        name__in=[
            "tofu",
            "chilled",
            "savoury_snacks",
            "sweet_snacks",
            "vegan_cheese",
            "powders",
            "flours_and_powders",
            "pantry_staples",
            "snacks_and_treats",
        ]
    )

    context = {
        "categories": categories,
    }

    return render(request, "homepage/index.html", context)
