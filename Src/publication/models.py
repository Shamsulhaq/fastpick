from django.db import models

from django.db.models.signals import pre_save

from fastpick.utils import unique_slug_generator
from tag.models import Tag


class PublicationManager(models.Manager):
    def get_publication(self):
        return self.get_queryset().all()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            instance = qs.first()
        return instance


# Create your models here.
class Publication(models.Model):
    name = models.CharField(max_length=150,unique=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True,allow_unicode=True)

    objects = PublicationManager()

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name


def pub_pre_save_reciver(sender, instance, *args, **kwargs):
    qs = Tag.objects.filter(keyword=instance.name)
    if qs.count() == 1:
        pass
    else:
        Tag.objects.create(keyword=instance.name)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(pub_pre_save_reciver, sender=Publication)
