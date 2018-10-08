from django.db import models
from carts.models import Cart

# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)


class Order(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=50.00, decimal_places=2, max_digits=9)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)

    def __str__(self):
        return self.order_id
