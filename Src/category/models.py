from django.db import models
from django.db.models.signals import pre_save

# Create your models here.
from fastpick.utils import unique_slug_generator


class Category(models.Model):
    keyword = models.CharField(max_length=155,help_text='Enter Tag keyword')
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, null=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword

    @property
    def title(self):
        return self.keyword


def tag_pre_save_reciver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_reciver, sender=Category)
