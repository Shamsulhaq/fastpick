from django.db import models
from django.db.models.signals import pre_save

# Create your models here.
from fastpick.utils import unique_slug_generator
from tag.models import Tag


class CategoryManager(models.Manager):
    def get_category(self):
        return self.get_queryset().all()

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            instance = qs.first()
        return instance


class Category(models.Model):
    keyword = models.CharField(max_length=155, help_text='Enter Tag keyword', unique=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, null=True, unique=True, allow_unicode=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ['keyword']

    objects = CategoryManager()

    @property
    def title(self):
        return self.keyword


def tag_pre_save_reciver(sender, instance, *args, **kwargs):
    Tag.objects.create(keyword=instance.keyword)
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_reciver, sender=Category)
