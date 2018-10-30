from django import forms

from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            # 'billing_profile',
            # 'address_type',
            'full_name',
            'phone',
            'address_line_1',
            'city',
            'country',
            'postal_code',
        ]

