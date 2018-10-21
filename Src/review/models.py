import os
import random

from django.core.files.storage import FileSystemStorage
from django.db import models


# Create your models here.
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.urls import reverse

from fastpick.utils import unique_slug_generator
fs = FileSystemStorage(location='media')


# To get extension from upload file
def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Book image with new name by function
def upload_review_image_path(inistance, file_name):
    book_name = slugify(inistance.book)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"Review/{book_name}/{final_filename}"


class ReviewManager(models.Manager):
    def all(self):
        return self.get_queryset().filter(active=True)

    def get_by_slug(self,slug):
        qs= self.get_queryset().filter(slug= slug)
        if qs.count()==1:
            return qs.first()
        return qs


class Review(models.Model):
    book = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_review_image_path, blank=True)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    update = models.DateTimeField(auto_now_add=False, auto_now=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True, null=True, allow_unicode=True)

    objects = ReviewManager()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return self.book

    @property
    def title(self):
        return self.book

    def get_absolute_url(self):
        return reverse('review-detail-view-url', kwargs={'slug': self.slug})


def review_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(review_pre_save_receiver, sender=Review)