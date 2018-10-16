from math import fsum
from django.db import models
from django.db.models.signals import pre_save, post_save
from addresses.models import Address
from billing.models import BillingProfile
from carts.models import Cart
from fastpick.utils import unique_order_id_generator

# Create your models here.

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('submit', 'Submit'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded')
)
SHIPPING_METHOD = (
    ('home delivery', 'Home Delivery'),
    ('office pick', 'Office Pick')
)


class ShippingMethod(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, blank=True, null=True)
    method = models.CharField(max_length=100, choices=SHIPPING_METHOD, default='home delivery')

    def __str__(self):
        return self.method


class OrderManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            cart=cart_obj,
            active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                cart=cart_obj)
            created = True
        return obj, created


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.CharField(max_length=120, blank=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.CASCADE, blank=True,
                                        null=True)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.CASCADE, blank=True,
                                         null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    def __str__(self):
        return self.order_id

    def update_shopping_cost(self):
        if self.shipping_method.method == 'home delivery':
            city = self.shipping_address.city
            cost = 50.00
            if city == 'Dhaka' or city == 'dhaka':
                cost = 50.00
            else:
                cost = 100.00
            self.shipping_total = cost
        else:
            cost = 0.00
        return cost

    def update_total(self):
        cart_total = self.cart.total
        shipping_total = self.shipping_total
        new_total = format(fsum([cart_total, shipping_total]), '.2f')
        self.total = new_total
        # self.save()
        return new_total

    def check_done(self):
        billing_profile = self.billing_profile
        billing_address = self.billing_address
        total = self.total
        if billing_address and billing_profile and total > 0:
            return True
        return False

    def mark_submit(self):
        if self.check_done():
            self.status = 'submit'
            self.save()
        return self.status


def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    # instance.shipping_total = shipping_cost_genaretor(instance)
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)

    if instance.shipping_address:
        instance.update_shopping_cost()
    if instance.shipping_address and instance.billing_address:
        instance.update_total()


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()
            order_obj.save()


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
        instance.save()

    # qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    # if qs.exists():
    #     qs.update(active=False)


pre_save.connect(pre_save_order_id_receiver, sender=Order)
post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, sender=Order)
