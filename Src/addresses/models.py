from django.db import models
from billing.models import BillingProfile

# Create your models here.
ADDRESS_TYPE = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping')
)


class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    full_name = models.CharField(max_length=155)
    phone = models.CharField(max_length=15)
    address_line_1 = models.CharField(max_length=120)
    city = models.CharField(max_length=120, default='Dhaka')
    country = models.CharField(max_length=120, default='Bangladesh')
    postal_code = models.CharField(max_length=120)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.address_line_1

    def get_address(self):
        return "{full_name}\n{address1}\n{city}\n{postal}\n{country}".format(
            full_name= self.full_name,
            address1=self.address_line_1,
            city=self.city,
            postal=self.postal_code,
            country=self.country
        )
