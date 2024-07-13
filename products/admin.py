from django.contrib import admin
from .models import Product, Category, NutritionalFacts, RelatedProduct, FastFact


class NutritionalFactsInline(admin.TabularInline):
    model = NutritionalFacts
    extra = 1 

class RelatedProductInline(admin.TabularInline):
    model = RelatedProduct
    fk_name = 'product'
    verbose_name_plural = 'Related Products'

class FastFactInline(admin.TabularInline):
    model = FastFact
    fk_name = 'product'
    verbose_name_plural = 'Fast Facts'


class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'sku',
        'name',
        'get_categories',
        'price',
        'rating',
        'image',
    )

    ordering = ('sku', )

    inlines = [
        NutritionalFactsInline,
        RelatedProductInline,
        FastFactInline,
    ] 

    def get_categories(self, obj):
        return ", ".join([category.name for category in obj.category.all()])
    get_categories.short_description = 'Categories'


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'friendly_name',
        'name',
    )


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)

