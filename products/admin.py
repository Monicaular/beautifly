from django.contrib import admin
from .models import Product, Category, NutritionalFacts, RelatedProduct, FastFact


class NutritionalFactsInline(admin.TabularInline):
    """Inline admin class for managing nutritional facts within a product."""

    model = NutritionalFacts
    extra = 1


class RelatedProductInline(admin.TabularInline):
    """Inline admin class for managing related products within a product."""

    model = RelatedProduct
    fk_name = "product"
    verbose_name_plural = "Related Products"


class FastFactInline(admin.TabularInline):
    """Inline admin class for managing fast facts within a product."""

    model = FastFact
    fk_name = "product"
    verbose_name_plural = "Fast Facts"


class ProductAdmin(admin.ModelAdmin):
    """Admin class for managing Product objects."""

    list_display = (
        "sku",
        "name",
        "get_categories",
        "price",
        "rating",
        "image",
    )

    ordering = ("sku",)

    inlines = [
        NutritionalFactsInline,
        RelatedProductInline,
        FastFactInline,
    ]

    def get_categories(self, obj):
        """Return a comma-separated list of categories for the product."""
        return ", ".join([category.name for category in obj.category.all()])

    get_categories.short_description = "Categories"


class CategoryAdmin(admin.ModelAdmin):
    """Admin class for managing Category objects."""

    list_display = (
        "friendly_name",
        "name",
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
