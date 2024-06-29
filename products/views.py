from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category

def all_products(request):
    """ A view to display all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    selected_categories = [] 
    sort = None
    direction = None

    categories = Category.objects.all()

    if request.GET:
        if 'sort' in request.GET:
            sort = request.GET['sort']
            sort_key = sort
            if sort == 'name':
                products.annotate(lower_mane=Lower('name'))
                sort_key = 'lower_name'
            if sort_key == 'category':
                sort_key = 'category__name'
            
            direction = request.GET.get('direction', 'asc')
            if direction == 'desc':
                sort_key = f'-{sort_key}'
            products = products.order_by(sort_key)

        if 'category' in request.GET:
            categories= request.GET['category'].split(',')
            products = products.filter(category__name__in=categories).distinct()
            categories = Category.objects.filter(name__in=categories)

        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You need to enter a search criteria!")
                return redirect (reverse('products'))
            
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'selected_categories': selected_categories,
        'categories': categories,  # Pass all categories to the template
        'current_sorting': current_sorting,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to display individual product details """

    product = get_object_or_404(Product, pk=product_id)
    categories = product.category.all()

    context = {
        'product': product,
        'categories': categories,
    }

    return render(request, 'products/product_detail.html', context)


