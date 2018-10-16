from django import forms
from .models import ShippingMethod


class ShippingMethodForm(forms.ModelForm):
    class Meta:
        model = ShippingMethod
        fields = ['method']
