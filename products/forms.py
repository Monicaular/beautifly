from django import forms
from .models import (
    Product,
    Category,
    NutritionalFacts,
    RelatedProduct,
    FastFact,
    Rating,
)
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    """Form for creating and updating Product objects."""

    class Meta:
        model = Product
        exclude = ["rating"]

        image = forms.ImageField(
            label="Image", required=False, widget=CustomClearableFileInput
        )

    def __init__(self, *args, **kwargs):
        """Initialize form, customize category choices and apply CSS classes."""
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields["category"].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "stripe-style-input"


class RatingForm(forms.ModelForm):
    """Form for submitting a rating for a product."""

    class Meta:
        model = Rating
        fields = ["value"]
        widgets = {
            "value": forms.HiddenInput(),
        }


class NutritionalFactsForm(forms.ModelForm):
    """Form for creating and updating NutritionalFacts objects."""

    class Meta:
        model = NutritionalFacts
        fields = ["name", "amount", "unit"]


class RelatedProductForm(forms.ModelForm):
    """Form for managing related products within a product."""

    class Meta:
        model = RelatedProduct
        fields = ["related_product"]


class FastFactForm(forms.ModelForm):
    """Form for managing fast facts related to a product."""

    class Meta:
        model = FastFact
        fields = ["fact"]
