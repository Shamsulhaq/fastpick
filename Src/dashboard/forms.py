from django import forms
from billing.models import BillingProfile


class BillingProfileForm(forms.ModelForm):
    class Meta:
        model = BillingProfile

        fields = (
             'full_name', 'email', 'phone', 'nid'
        )