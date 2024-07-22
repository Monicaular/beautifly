from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.db.models.functions import Lower
from .models import Product, Category, NutritionalFacts, RelatedProduct, FastFact
from .forms import ProductForm, NutritionalFactsForm, RelatedProductForm, FastFactForm
from urllib.parse import urlencode
from django.forms.models import inlineformset_factory




def all_products(request):
    """ A view to display all products, including sorting and search queries """

    products = Product.objects.all()
    query = None
    selected_categories = [] 
    sort = None
    direction = None

    categories = Category.objects.all()

    qd = request.GET.copy()
    qd.pop('page', None)
    querystring = qd.urlencode()

    
    if 'sort' in request.GET:
        sort = request.GET['sort']
        sort_key = sort

        if sort == 'name':
            products = products.annotate(lower_name=Lower('name'))
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
        if query:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
        else:
            messages.error(request, "You need to enter a search criteria!")
            return redirect (reverse('products'))
        
    # Pagination setup
    paginator = Paginator(products, 12) 
    page_number = request.GET.get('page')
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)  

    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'selected_categories': selected_categories,
        'categories': categories, 
        'current_sorting': current_sorting,
        'query': query,
        'querystring': querystring,
    }

    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to display individual product details """

    product = get_object_or_404(Product, pk=product_id)
    categories = product.category.all()
    nutritional_facts = product.nutritional_facts.all()
    related_products = product.related_products.all()
    fast_facts = product.fast_facts.all()
    
    context = {
        'product': product,
        'categories': categories,
        'nutritional_facts': nutritional_facts,
        'related_products': related_products,
        'interesting_facts': fast_facts,

    }

    return render(request, 'products/product_detail.html', context)

def add_product(request):
    NutritionalFactsFormSet = inlineformset_factory(Product, NutritionalFacts, form=NutritionalFactsForm, extra=1)
    RelatedProductFormSet = inlineformset_factory(Product, RelatedProduct, form=RelatedProductForm, fk_name='product', extra=1)
    FastFactFormSet = inlineformset_factory(Product, FastFact, form=FastFactForm, extra=1)

    if request.method == 'POST':
        product_form = ProductForm(request.POST, request.FILES)
        product = product_form.save(commit=False)
        nutritional_formset = NutritionalFactsFormSet(request.POST, instance=product)
        related_formset = RelatedProductFormSet(request.POST, instance=product)
        fast_fact_formset = FastFactFormSet(request.POST, instance=product)

        if product_form.is_valid() and nutritional_formset.is_valid() and related_formset.is_valid() and fast_fact_formset.is_valid():
            product.save()
            nutritional_formset.instance = product
            nutritional_formset.save()
            related_formset.instance = product
            related_formset.save()
            fast_fact_formset.instance = product
            fast_fact_formset.save()
            return redirect('products')
    else:
        product_form = ProductForm()
        nutritional_formset = NutritionalFactsFormSet()
        related_formset = RelatedProductFormSet()
        fast_fact_formset = FastFactFormSet()

    context = {
        'product_form': product_form,
        'nutritional_formset': nutritional_formset,
        'related_formset': related_formset,
        'fast_fact_formset': fast_fact_formset,
    }
    return render(request, 'products/add_product.html', context)