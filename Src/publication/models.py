from django.db import models

from django.db.models.signals import pre_save

from fastpick.utils import unique_slug_generator


# Create your models here.
class Publication(models.Model):
    name = models.CharField(max_length=150)
    info = models.TextField()
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name


def pub_pre_save_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pub_pre_save_reciver, sender=Publication)