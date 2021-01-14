from django import forms
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # First call default init method, set form as it would be by default
        super().__init__(*args, **kwargs)
        # Dict of placeholders which will appear in the form fields
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # Set autofocus attribute on the full name field
        self.fields['full_name'].widget.attrs['autofocus'] = True
        # iterate through the forms fields
        for field in self.fields:
            if self.fields[field].required:
                # adding a star if field required
                placeholder = f'{placeholders[field]} *'
            else:
                placeholder = placeholders[field]
            # setting all placeholders to their values in above dictionary
            self.fields[field].widget.attrs['placeholder'] = placeholder
            # Add a CSS class called striped-style-input
            self.fields[field].widget.attrs['class'] = 'striped-style-input'
            # Removing the form fields labels
            self.fields[field].label = False
