from django.db import models
from django.db.models.signals import pre_save, post_save

PAYMENT_STATUS_CHOICES = (
    ('unpaid', 'UnPaid'),
    ('paid', 'Paid'),
    ('pending', 'Pending'),
    ('failed', 'Failed'),
    ('refunded', 'Refunded')
)

PAYMENT_METHOD_CHOICES = (
    ('bkash', 'Bkash'),
    ('rocket', 'Rocket'),
    ('cash', 'Cash'),
)


class RequestPaymentManager(models.Manager):

    def get_by_order_id(self, id):
        qs = self.get_queryset().filter(order_id=id)
        if qs.count() == 1:
            return qs.first()


# Create your models here.
class RequestPayment(models.Model):
    order_id = models.CharField(max_length=10, unique=True)
    payment_by = models.CharField(max_length=120, choices=PAYMENT_METHOD_CHOICES)
    txn_id = models.CharField(max_length=20)
    phone = models.CharField(max_length=15)
    amount = models.DecimalField(default=0.00, decimal_places=0, max_digits=9)
    status = models.CharField(max_length=120, default='unpaid', choices=PAYMENT_STATUS_CHOICES)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.order_id

    class Meta:
        ordering = ['-timestamp']

    objects = RequestPaymentManager()


# def pre_save_receiver(sender, instance, *args, **kwargs):
#     if instance.txn_id and instance.phone:
#         instance.status = 'pending'
#
#
# pre_save.connect(pre_save_receiver, sender=RequestPayment)


def post_save_receiver(sender, created, instance, *args, **kwargs):
    if not created:
        if instance.txn_id and instance.phone:
            instance.status = 'pending'


post_save.connect(post_save_receiver, sender=RequestPayment)
