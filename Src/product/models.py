import os
import random

from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save
# from main app - fastpick
from django.template.defaultfilters import slugify

from fastpick.utils import unique_slug_generator
# from local app --
from tag.models import Tag
from category.models import Category
from publication.models import Publication

fs = FileSystemStorage(location='media')


# To get extension from upload file
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


# To save Book image with new name by function
def upload_book_image_path(inistance, file_name):
    book_name = slugify(inistance.name)
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = f'{new_filename}{ext}'
    return f"Book/{book_name}/{final_filename}"


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


class BookQuerySet(models.query.QuerySet):
    def active(self):  # for check is Activ
        return self.filter(active=True)

    def is_stock(self):  # for check is Stock Available
        return self.filter(is_stock=True)

    def is_rent_available(self):  # for check Rent Available
        return self.filter(is_rent_available=True)

    def search(self, keyword):
        lookups = (
                Q(name__icontains=keyword) |
                Q(descriptions__icontains=keyword) |
                Q(category__keyword__icontains=keyword) |
                Q(publication__name__icontains=keyword) |
                Q(author__name__icontains=keyword) |
                Q(author__bio__icontains=keyword) |
                Q(tag__keyword__icontains=keyword))

        return self.active().filter(lookups).distinct()


class BookManager(models.Manager):
    def get_queryset(self):
        return BookQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def is_stock(self):
        return self.get_queryset().is_stock()

    def is_rent_available(self):
        return self.get_queryset().is_rent_available()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return qs

    def get_by_slug(self, slug):
        qs = self.get_queryset().filter(slug=slug)
        if qs.count() == 1:
            return qs.first()

    def search(self, query):
        return self.get_queryset().search(keyword=query)


class BookList(models.Model):
    name = models.CharField(max_length=255, help_text="Enter Book Name")
    author = models.ForeignKey(BookAuthor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE)
    publish_date = models.CharField(max_length=4, help_text='Year eg. 1998 , 2018')
    total_pages = models.PositiveIntegerField(blank=True,null=True)
    regular_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descriptions = models.TextField()
    rent_charge = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    image = models.ImageField(upload_to=upload_book_image_path, blank=True)
    tag = models.ManyToManyField(Tag)
    is_old = models.BooleanField(default=True)
    is_stock = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    is_rent_available = models.BooleanField(default=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

    objects = BookManager()

    class Meta:
        ordering = ['-timeStamp']

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name

    def get_rent_charge(self):
        dis = (self.price * 15) / 100
        return dis

    def get_discount(self):
        if self.regular_price == 0:
            discount = 0
        else:
            discount = (self.regular_price - self.price) / self.regular_price * 100

        discount = int(discount)
        return str(discount) + '%'

    def get_absolute_url(self):
        return "/book/detail/{slug}".format(slug = self.slug)


def bl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

    if instance.is_rent_available:
        instance.rent_charge = (instance.price * 15) / 100
    else:
        instance.rent_charge = 0


pre_save.connect(bl_pre_save_receiver, sender=BookList)


def ba_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(ba_pre_save_receiver, sender=BookAuthor)
