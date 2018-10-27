from django.db import models
from django.conf import settings
from datetime import date,timedelta
from django.db.models.signals import m2m_changed, pre_save, post_save

from billing.models import BillingProfile
from fastpick.utils import unique_order_id_generator
from product.models import BookList

# Create your models here.
User = settings.AUTH_USER_MODEL


class RentCartManager(models.Manager):

    def new_or_get(self, request):
        rent_id = request.session.get("rent_id", None)
        qs = self.get_queryset().filter(id=rent_id)
        if qs.count() == 1:
            new_obj = False
            rent_obj = qs.first()
            if request.user.is_authenticated and rent_obj.user is None:
                rent_obj.user = request.user
                rent_obj.save()
        else:
            rent_obj = RentCart.objects.new(user=request.user)
            new_obj = True
            request.session['rent_id'] = rent_obj.id
        return rent_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


class RentCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    books = models.ManyToManyField(BookList, blank=True)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = RentCartManager()

    def __str__(self):
        return str(self.id)


def m2m_save_rent_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.books.all()
        total = 0
        for x in products:
            total += x.rent_charge
        instance.total = total
        instance.save()


m2m_changed.connect(m2m_save_rent_receiver, sender=RentCart.books.through)

# Rent MOdel
ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('submit', 'Submit'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('returned', 'Returned')
)


class RentManager(models.Manager):
    def new_or_get(self, billing_profile, cart_obj):
        created = False
        qs = self.get_queryset().filter(
            billing_profile=billing_profile,
            rent_cart=cart_obj,
            active=True, status='created')
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                billing_profile=billing_profile,
                rent_cart=cart_obj)
            created = True
        return obj, created

    # for User DashBoard
    def get_rent_paid(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile, status='paid')
        return qs

    def get_all_rent(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile).exclude(status='created')
        if qs.count() == 1:
            return qs
        return qs

    def get_all_pending(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile, status='submit' or 'paid')
        return qs

    def get_all_done(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile, status='shipped')
        return qs

    def get_all_return(self, billing_profile):
        qs = self.get_queryset().filter(billing_profile__user=billing_profile, status='returned')
        return qs


class Rent(models.Model):
    order_id = models.CharField(max_length=120, blank=True)
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE, blank=True, null=True)
    rent_cart = models.ForeignKey(RentCart, on_delete=models.CASCADE)
    status = models.CharField(max_length=120, default='created', choices=ORDER_STATUS_CHOICES)
    total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
    receive_date = models.DateField(blank=True, null=True)
    return_date = models.DateField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    active = models.BooleanField(default=True)

    objects = RentManager()

    class Meta:
        ordering = ['-return_date']

    def __str__(self):
        return str(self.id)

    def update_total(self):
        cart_total = self.rent_cart.total
        self.total = cart_total
        # self.save()
        return cart_total

    def check_done(self):
        billing_profile = self.billing_profile
        total = self.total
        if billing_profile and total > 0:
            return True
        return False

    def mark_submit(self):
        if self.check_done():
            self.status = 'submit'
            self.save()
        return self.status


def pre_save_order_id_receiver(sender, instance, *args, **kwargs):
    if not instance.order_id:
        instance.order_id = unique_order_id_generator(instance)
    instance.update_total()
    if instance.receive_date:
        instance.status = 'shipped'
        instance.return_date = (instance.receive_date+timedelta(days=7)).isoformat()

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


def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_id = cart_obj.id
        qs = Rent.objects.filter(cart__id=cart_id)
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


pre_save.connect(pre_save_order_id_receiver, sender=Rent)
# post_save.connect(post_save_cart_total, sender=RentCart)
post_save.connect(post_save_order, sender=Rent)
