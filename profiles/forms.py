from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information, excluding the user field.
    Adds placeholders, classes, and autofocus to form fields.
    """

    class Meta:
        model = UserProfile
        exclude = ("user",)

    def __init__(self, *args, **kwargs):
        """
        Customize form fields with placeholders, CSS classes,
        and autofocus on the phone number field.
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            "default_full_name": "Full Name",
            "default_phone_number": "Phone Number",
            "default_postcode": "Postal Code",
            "default_town_or_city": "Town or City",
            "default_street_address1": "Street Address 1",
            "default_street_address2": "Street Address 2",
            "default_county": "County, State or Locality",
        }

        self.fields["default_phone_number"].widget.attrs["autofocus"] = True
        for field in self.fields:
            if field != "default_country":
                if self.fields[field].required:
                    placeholder = f"{placeholders[field]} *"
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs["placeholder"] = placeholder
            self.fields[field].widget.attrs["class"] = "stripe-style-input"
            self.fields[field].label = False
