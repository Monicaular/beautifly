from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError, transaction
from django.db.models import Q
from django.db.models.functions import Lower
from .models import (
    Product,
    Category,
    NutritionalFacts,
    RelatedProduct,
    FastFact,
    Rating,
)
from .forms import (
    ProductForm,
    NutritionalFactsForm,
    RelatedProductForm,
    FastFactForm,
    RatingForm,
)
from urllib.parse import urlencode
from django.forms.models import inlineformset_factory


def all_products(request):
    """Display all products with options for sorting and search queries."""

    products = Product.objects.all()
    query = None
    selected_categories = []
    sort = None
    direction = None
    categories = Category.objects.all()

    qd = request.GET.copy()
    qd.pop("page", None)
    querystring = qd.urlencode()

    if "sort" in request.GET:
        sort = request.GET["sort"]
        sort_key = sort

        if sort == "name":
            products = products.annotate(lower_name=Lower("name"))
            sort_key = "lower_name"

        if sort_key == "category":
            sort_key = "category__name"

        direction = request.GET.get("direction", "asc")

        if direction == "desc":
            sort_key = f"-{sort_key}"

        products = products.order_by(sort_key)

    if "category" in request.GET:
        categories = request.GET["category"].split(",")
        products = products.filter(category__name__in=categories).distinct()
        categories = Category.objects.filter(name__in=categories)

    if "q" in request.GET:
        query = request.GET["q"]
        if query:
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
        else:
            messages.error(request, "You need to enter a search criteria!")
            return redirect(reverse("products"))

    # Pagination setup
    paginator = Paginator(products, 12)
    page_number = request.GET.get("page")
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    current_sorting = f"{sort}_{direction}"

    context = {
        "products": products,
        "selected_categories": selected_categories,
        "categories": categories,
        "current_sorting": current_sorting,
        "query": query,
        "querystring": querystring,
    }

    return render(request, "products/products.html", context)


def product_detail(request, product_id):
    """Display details of an individual product."""

    product = get_object_or_404(Product, pk=product_id)
    categories = product.category.all()
    ratings = product.ratings.all()
    nutritional_facts = product.nutritional_facts.all()
    related_products = product.related_products.all()
    fast_facts = product.fast_facts.all()

    rating_form = RatingForm()

    heart_labels = [
        (1, "Poor"),
        (2, "Quite Good"),
        (3, "Good"),
        (4, "Very Good"),
        (5, "Excellent"),
    ]

    context = {
        "product": product,
        "categories": categories,
        "rating_form": rating_form,
        "heart_labels": heart_labels,
        "ratings": ratings,
        "nutritional_facts": nutritional_facts,
        "related_products": related_products,
        "interesting_facts": fast_facts,
    }

    return render(request, "products/product_detail.html", context)


@login_required
def add_product(request):
    """Allow store owners to add a new product."""

    if not request.user.is_superuser:
        messages.error(
            request,
            "Access denied: Only store owners are authorized to perform this action.",
        )
        return redirect(reverse("home"))

    NutritionalFactsFormSet = inlineformset_factory(
        Product, NutritionalFacts, form=NutritionalFactsForm, extra=1, can_delete=True
    )
    RelatedProductFormSet = inlineformset_factory(
        Product,
        RelatedProduct,
        form=RelatedProductForm,
        fk_name="product",
        extra=1,
        can_delete=True,
    )
    FastFactFormSet = inlineformset_factory(
        Product, FastFact, form=FastFactForm, extra=1, can_delete=True
    )

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES)
        nutritional_formset = NutritionalFactsFormSet(request.POST)
        related_formset = RelatedProductFormSet(request.POST)
        fast_fact_formset = FastFactFormSet(request.POST)

        if product_form.is_valid():
            product = product_form.save(commit=False)
            nutritional_formset.instance = product
            related_formset.instance = product
            fast_fact_formset.instance = product

            if (
                nutritional_formset.is_valid()
                and related_formset.is_valid()
                and fast_fact_formset.is_valid()
            ):
                try:
                    product.save()

                    nutritional_formset.save()

                    related_formset.save()

                    fast_fact_formset.save()
                    messages.success(request, "Product added successfully!")
                    return redirect(reverse("product_detail", args=[product.id]))
                except ValueError as e:
                    messages.error(request, f"Error: {str(e)}")
            else:
                messages.error(request, "Please correct the errors below.")

        else:
            messages.error(request, "Please correct the errors in the main form below.")

    else:
        product_form = ProductForm()
        nutritional_formset = NutritionalFactsFormSet()
        related_formset = RelatedProductFormSet()
        fast_fact_formset = FastFactFormSet()

    context = {
        "product_form": product_form,
        "nutritional_formset": nutritional_formset,
        "related_formset": related_formset,
        "fast_fact_formset": fast_fact_formset,
    }
    return render(request, "products/add_product.html", context)


@login_required
def edit_product(request, product_id):
    """Allow store owners to edit an existing product."""

    if not request.user.is_superuser:
        messages.error(
            request,
            "Access denied: Only store owners are authorized to perform this action.",
        )
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)
    NutritionalFactsFormSet = inlineformset_factory(
        Product, NutritionalFacts, form=NutritionalFactsForm, extra=1, can_delete=True
    )
    RelatedProductFormSet = inlineformset_factory(
        Product,
        RelatedProduct,
        form=RelatedProductForm,
        fk_name="product",
        extra=1,
        can_delete=True,
    )
    FastFactFormSet = inlineformset_factory(
        Product, FastFact, form=FastFactForm, extra=1, can_delete=True
    )

    if request.method == "POST":
        product_form = ProductForm(request.POST, request.FILES, instance=product)
        nutritional_formset = NutritionalFactsFormSet(request.POST, instance=product)
        related_formset = RelatedProductFormSet(request.POST, instance=product)
        fast_fact_formset = FastFactFormSet(request.POST, instance=product)

        if (
            product_form.is_valid()
            and nutritional_formset.is_valid()
            and related_formset.is_valid()
            and fast_fact_formset.is_valid()
        ):
            try:
                product = product_form.save()
                for form in nutritional_formset:
                    if form.cleaned_data.get("DELETE"):
                        form.instance.delete()
                    elif form.has_changed():
                        form.save()

                for form in related_formset:
                    if form.cleaned_data.get("DELETE"):
                        form.instance.delete()
                    elif form.has_changed():
                        form.save()

                for form in fast_fact_formset:
                    if form.cleaned_data.get("DELETE"):
                        form.instance.delete()
                    elif form.has_changed():
                        form.save()

                messages.success(request, "Successfully updated product!")
                return redirect("product_detail", product_id=product.id)
            except ValueError as e:
                messages.error(request, f"Error: {str(e)}")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        product_form = ProductForm(instance=product)
        nutritional_formset = NutritionalFactsFormSet(instance=product)
        related_formset = RelatedProductFormSet(instance=product)
        fast_fact_formset = FastFactFormSet(instance=product)
        messages.info(request, f"You are editing {product.name}")

    context = {
        "product_form": product_form,
        "nutritional_formset": nutritional_formset,
        "related_formset": related_formset,
        "fast_fact_formset": fast_fact_formset,
        "product": product,
    }

    return render(request, "products/edit_product.html", context)


@login_required
def delete_product(request, product_id):
    """Allow store owners to delete a product from the store."""

    if not request.user.is_superuser:
        messages.error(
            request,
            "Access denied: Only store owners are authorized to perform this action.",
        )
        return redirect(reverse("home"))

    product = get_object_or_404(Product, pk=product_id)

    product.delete()
    messages.success(request, "Product deleted successfully!")
    return redirect(reverse("products"))


@login_required
def add_rating(request, product_id):
    """Allow users to submit a rating for a product."""

    product = get_object_or_404(Product, pk=product_id)

    if request.method == "POST":
        # Check if the user has already rated this product
        if Rating.objects.filter(product=product, user=request.user).exists():
            messages.error(request, "You have already rated this product.")
            return redirect(reverse("product_detail", args=[product.id]))

        rating_form = RatingForm(request.POST)

        if rating_form.is_valid():
            try:
                with transaction.atomic():
                    # Create and save the rating
                    rating = rating_form.save(commit=False)
                    rating.product = product
                    rating.user = request.user
                    rating.save()

                messages.success(
                    request, "Your rating has been successfully submitted!"
                )
                return redirect(reverse("product_detail", args=[product.id]))
            except IntegrityError as e:
                messages.error(
                    request, "An error occurred while submitting your rating."
                )
                return redirect(reverse("product_detail", args=[product.id]))
        else:
            messages.error(request, "There was a problem with your rating submission.")

    return redirect(reverse("product_detail", args=[product.id]))
