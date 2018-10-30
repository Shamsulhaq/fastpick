from django import forms

from .models import RequestPayment


class RequestPaymentForm(forms.ModelForm):
    txn_id = forms.CharField(max_length=20)

    class Meta:
        model = RequestPayment
        fields = [
            'payment_by',
            'txn_id',
            'phone',
        ]

    def clean_txn_id(self):
        txn_id = self.cleaned_data.get("txn_id")
        qs = RequestPayment.objects.filter(txn_id=txn_id)
        if qs.exists():
            raise forms.ValidationError("This Txn ID is Invalid!")
        return txn_id