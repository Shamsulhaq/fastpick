from django.db import models
from django.db.models.signals import pre_save
# from main app - fastpick

from fastpick.utils import unique_slug_generator
# from local app --
from tag.models import Tag
from category.models import Category


class BookAuthor(models.Model):
    name = models.CharField(max_length=255, help_text="Enter Author name")
    image = models.ImageField(upload_to='Author/img', blank=True)
    bio = models.TextField()
    slug = models.SlugField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def title(self):
        return self.name


class BookList(models.Model):
    name = models.CharField(max_length=255, help_text="Enter Book Name")
    author = models.ForeignKey(BookAuthor, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    publish_date = models.CharField(max_length=4, help_text='Year eg. 1998 , 2018')
    last_edition_publish = models.CharField(max_length=4, help_text='Year eg. 1998 , 2018', blank=True, null=True)
    regular_price = models.DecimalField(max_digits=9, decimal_places=2, default=0, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    descriptions = models.TextField()
    rent_charge = models.DecimalField(max_digits=9, decimal_places=2, default=0)
    image = models.ImageField(upload_to="Book/img", blank=True)
    tag = models.ManyToManyField(Tag)
    is_stock = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    timeStamp = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(blank=True, null=True, unique=True)

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


def bl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
    instance.rent_charge = (instance.price * 15) / 100


pre_save.connect(bl_pre_save_receiver, sender=BookList)


def ba_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(ba_pre_save_receiver, sender=BookAuthor)
