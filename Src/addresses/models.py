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
    address_line_1 = models.CharField(max_length=120)
    address_line_2 = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120, default='Dhaka')
    country = models.CharField(max_length=120, default='Bangladesh')
    state = models.CharField(max_length=120, default='Bangladesh',null=True,blank='get_address')
    postal_code = models.CharField(max_length=120)

    def __str__(self):
        return self.address_line_1

    def get_address(self):
        return "{address1}\n{address2}\n{city}\n{state}, {postal}\n{country}".format(
            address1=self.address_line_1,
            address2=self.address_line_2 or "",
            city=self.city,
            state=self.state or "",
            postal=self.postal_code,
            country=self.country
        )
