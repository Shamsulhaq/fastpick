from django.conf import settings
from django.db import models
from django.db.models.signals import post_save

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL


# Create your models here.


class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        user = request.user
        guest_email_id = request.session.get('guest_email_id')
        guest_phone = request.session.get('guest_phone')
        obj = None
        created = False

        if user.is_authenticated:
            # logged in user checkout ;
            obj, created = self.model.objects.get_or_create(user=user, email=user.email)
        elif guest_email_id is not None:
            # guest user checkout;
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(
                email=guest_email_obj.email, phone=guest_phone)
        else:
            pass

        return obj, created


class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    full_name = models.CharField(max_length=250, blank=True, null=True)
    email = models.EmailField()
    nid = models.CharField(max_length=17, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    active = models.BooleanField(default=True)
    verify = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email, full_name=instance.full_name)


post_save.connect(user_created_receiver, sender=User)
