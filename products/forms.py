from django import forms
from .models import Product, Category, NutritionalFacts, RelatedProduct, FastFact



class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'stripe-style-input'

class NutritionalFactsForm(forms.ModelForm):
    class Meta:
        model = NutritionalFacts
        fields = ['name', 'amount', 'unit']

class RelatedProductForm(forms.ModelForm):
    class Meta:
        model = RelatedProduct
        fields = ['related_product']

class FastFactForm(forms.ModelForm):
    class Meta:
        model = FastFact
        fields = ['fact']