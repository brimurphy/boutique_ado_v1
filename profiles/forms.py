from django import forms
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # First call default init method, set form as it would be by default
        super().__init__(*args, **kwargs)
        # Dict of placeholders which will appear in the form fields
        placeholders = {
            'default_phone_number': 'Phone Number',
            'default_postcode': 'Postal Code',
            'default_town_or_city': 'Town or City',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_county': 'County, State or Locality',
        }

        # Set autofocus attribute on the full name field
        self.fields['default_phone_number'].widget.attrs['autofocus'] = True
        # iterate through the forms fields
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    # adding a star if field required
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                # setting all placeholders to their values in above dictionary
                self.fields[field].widget.attrs['placeholder'] = placeholder
            # Add a CSS class called striped-style-input
            self.fields[field].widget.attrs['class'] =\
                'border-black rounded-0 profile-form-input'
            # Removing the form fields labels
            self.fields[field].label = False
