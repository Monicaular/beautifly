from django.contrib import admin
from .models import CarouselItem

@admin.register(CarouselItem)
class CarouselItemAdmin(admin.ModelAdmin):
    list_display = ('caption_title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('image', 'caption_title', 'caption_text', 'title_link', 'text_link', 'is_active',)


