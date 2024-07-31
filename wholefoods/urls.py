from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404
from django.conf.urls import handler500
from django.views.generic import TemplateView
from .views import custom_404_page, custom_500_page
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("about/", views.about_us, name="about_us"),
    path("privacy-policy/", views.privacy_policy, name="privacy-policy"),
    path(
        "delivery-terms/",
        TemplateView.as_view(template_name="delivery_terms.html"),
        name="delivery_terms",
    ),
    path(
        "quality_guarantee/",
        TemplateView.as_view(template_name="quality_guarantee.html"),
        name="quality_guarantee",
    ),
    path("accounts/", include("allauth.urls")),
    path("", include("homepage.urls")),
    path("products/", include("products.urls")),
    path("basket/", include("basket.urls")),
    path("checkout/", include("checkout.urls")),
    path("profile/", include("profiles.urls")),
    path("wishlist/", include("wishlist.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = custom_404_page
handler500 = custom_500_page
