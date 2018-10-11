import os
import random
from django.core.files.storage import FileSystemStorage
from django.template.defaultfilters import slugify

from django.db import models

fs = FileSystemStorage(location='media')
# Create your models here.


def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


# To save Book image with new name by function
def complain_image_upload_path(inistance, file_name):
    person = slugify(inistance.name)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"Complain/{person}/{final_filename}"


class Contact(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    massage = models.TextField()

    def __str__(self):
        self.name


COMPLAIN_CHOOSE = (
    ('sd', 'Slow delivery'),
    ('pcs', 'Poor client service'),
    ('rs', 'Rude staff'),
    ('as', 'About service'),
    ('o', 'Others'),
)


class Complain(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    complain_type = models.CharField(max_length=5, choices=COMPLAIN_CHOOSE)
    massage = models.TextField()
    screenshots = models.ImageField(upload_to=complain_image_upload_path,blank=True,null=True)

    def __str__(self):
        return self.name