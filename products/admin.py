from django.contrib import admin
from .models import Product, Category, NutritionalFacts


class NutritionalFactsInline(admin.TabularInline):  # or admin.StackedInline for different layout
    model = NutritionalFacts
    extra = 1  # Number of extra forms to display

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

    inlines = [NutritionalFactsInline]  # Include the inline here

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
admin.site.register(NutritionalFacts)
