from math import fsum

from django.core.mail import EmailMessage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.template.loader import get_template

from addresses.models import Address
from billing.models import BillingProfile
from fastpick import settings
from fastpick.utils import unique_order_id_generator

# Create your models here.
from product.models import BookList

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
    def new_or_get(self, billing_profile):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
            )
            created = True
        return obj, created

    # for User DashBoard
    def get_order_paid(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile, status='paid')
        return qs

    def get_all_order(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile).exclude(status='created')
        if qs.count() == 1:
            return qs
        return qs

    def get_all_pending(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile, status='submit')
        return qs

    def get_all_done(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile, status='shipped')
        return qs


class Order(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, blank=True, null=True)
    order_id = models.CharField(max_length=120, blank=True)
    billing_address = models.ForeignKey(Address, related_name='billing_address', on_delete=models.CASCADE, blank=True,
                                        null=True)
    shipping_address = models.ForeignKey(Address, related_name='shipping_address', on_delete=models.CASCADE, blank=True,
                                         null=True)
    # cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    cart_total = models.DecimalField(default=0.00, decimal_places=0, max_digits=9)
    shipping_method = models.ForeignKey(ShippingMethod, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    shipping_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    total = models.DecimalField(default=0.00, decimal_places=0, max_digits=9)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    objects = OrderManager()

    class Meta:
        ordering = ['-timestamp']

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
        shipping_total = self.shipping_total
        order_items = OrderItem.objects.filter(order=self.id)
        total = 0
        for item in order_items:
            total += item.item_total
        new_total = format(fsum([total, shipping_total]), '.2f')
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
            self.book_order_count()

        return self.status

    def book_order_count(self):
        products = OrderItem.objects.filter(order=self.id)
        # print(products.all())
        for product in products.all():
            book_id = product.product.id
            # print(product.product.id)
            # print(product.quantity)
            book = BookList.objects.get_by_id(book_id)
            # print(book.order)
            book.order += product.quantity
            # print(book.order)
            book.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(BookList, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    item_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        total = self.price * self.quantity
        self.item_total = total
        # self.save()


def pre_save_order_item_receiver(sender, instance, *args, **kwargs):
    instance.get_cost()


pre_save.connect(pre_save_order_item_receiver, sender=OrderItem)


# def post_save_order_item_receiver(sender,created, instance, *args, **kwargs):
#     if created:
#         instance.book_order_count()
#
#
# post_save.connect(post_save_order_item_receiver, sender=OrderItem)
#

def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    # instance.shipping_total = shipping_cost_genaretor(instance)
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    if instance.cart_total == 0:
        order_items = OrderItem.objects.filter(order=instance.id)
        total = 0
        for item in order_items:
            total += item.item_total
        instance.cart_total = total
        instance.update_total()

    if instance.shipping_address:
        instance.update_shopping_cost()
    if instance.shipping_address and instance.billing_address:
        instance.update_total()

    # if instance.status == 'submit':
    #     pk = instance.id
    #     object = Order.objects.filter(id=pk)
    #     text = {
    #         'object': object,
    #     }
    #     print(object)
    #     print(text)
    #     mail_subject = 'Payment Successful'
    #     message = get_template('carts/success.html').render(text)
    #     to_email = instance.billing_profile.email
    #     email_from = settings.EMAIL_HOST_USER
    #     email = EmailMessage(
    #         mail_subject, message, email_from, to=[to_email]
    #     )
    #     email.content_subtype = 'html'
    #     print(to_email)
    #     email.send()


pre_save.connect(pre_save_order_id_receiver, sender=Order)


#
# def post_save_cart_total(sender, instance, created, *args, **kwargs):
#     if not created:
#         cart_obj = instance
#         cart_total = cart_obj.total
#         cart_id = cart_obj.id
#         qs = Order.objects.filter(cart__id=cart_id)
#         if qs.count() == 1:
#             order_obj = qs.first()
#             order_obj.update_total()
#             order_obj.save()


def post_save_order(sender, instance, created, *args, **kwargs):
    if created:
        instance.update_total()
        instance.save()

    # qs = Order.objects.filter(cart=instance.cart).exclude(billing_profile=instance.billing_profile)
    # if qs.exists():
    #     qs.update(active=False)


#
# pre_save.connect(pre_save_order_id_receiver, sender=Order)
# post_save.connect(post_save_cart_total, sender=Cart)
post_save.connect(post_save_order, sender=Order)
