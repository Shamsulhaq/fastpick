import os
import random

from django.db import models
from django.db.models.signals import pre_save

from fastpick.utils import unique_slug_generator
from django.template.defaultfilters import slugify


# Create your models here.
def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Author image with new name by function
def upload_author_image_path(inistance, file_name):
    author_name = slugify(inistance.name)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"Author/{author_name}/{final_filename}"


class BookAuthor(models.Model):
    name = models.CharField(max_length=255, help_text="Enter Author name")
    image = models.ImageField(upload_to=upload_author_image_path, blank=True)
    bio = models.TextField()
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name


def ba_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(ba_pre_save_receiver, sender=BookAuthor)