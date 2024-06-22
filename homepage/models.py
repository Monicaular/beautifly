from django.db import models

class CarouselItem(models.Model):
    image = models.ImageField(null=True, blank=True, upload_to='carousel/')
    caption_title = models.CharField(max_length=100, blank=True)
    caption_text = models.TextField(blank=True)
    title_link = models.URLField(max_length=200, blank=True)
    text_link = models.URLField(max_length=200, blank=True)
    is_active = models.BooleanField(default=False)


    def __str__(self):
        return self.caption_title or "Carousel Image"