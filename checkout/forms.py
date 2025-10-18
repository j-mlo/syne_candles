from django import forms 
from .models import Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number', 
                  'street_address1', 'street_address2', 
                  'town_or_city', 'postcode', 'country',)
        
    def __init__(self, *args, **kwargs):
        """ 
        Add placeholders and classes, remove auto-generated labels
        and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name', 
            'email': 'Email Address', 
            'phone_number': 'Phone Number', 
            'street_address1': 'Street Address 1', 
            'street_address2': 'Street Address 2', 
            'town_or_city': 'Town / City', 
            'postcode': 'Postal Code', 
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.field[field].required:
                    placeholder = f'{placeholders[field]} *'
                else: 
                    placeholder = placeholders[field]
                self.field[field].widget.attrs['placeholder'] = placeholder
            self.field[field].widget.attrs['class'] = 'stripe-style-input'
            self.field[field].label = False

