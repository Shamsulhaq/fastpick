# from math import fsum
# from decimal import Decimal
# from django.db import models
# from django.conf import settings
# from django.db.models.signals import m2m_changed, pre_save
#
# from product.models import BookList
#
# # Create your models here.
# User = settings.AUTH_USER_MODEL
#
#
# class Items(models.Model):
#     book = models.ForeignKey(BookList,on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
#     price = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
#     total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
#
#     def __str__(self):
#         return self.book.name
#
#     def item_total(self):
#         total = self.price * self.quantity
#         return total
#
#
# class CartManager(models.Manager):
#
#     def new_or_get(self, request):
#         cart_id = request.session.get("cart_id", None)
#         qs = self.get_queryset().filter(id=cart_id)
#         if qs.count() == 1:
#             new_obj = False
#             cart_obj = qs.first()
#             if request.user.is_authenticated and cart_obj.user is None:
#                 cart_obj.user = request.user
#                 cart_obj.save()
#         else:
#             cart_obj = Cart.objects.new(user=request.user)
#             new_obj = True
#             request.session['cart_id'] = cart_obj.id
#         return cart_obj, new_obj
#
#     def new(self, user=None):
#         user_obj = None
#         if user is not None:
#             if user.is_authenticated:
#                 user_obj = user
#         return self.model.objects.create(user=user_obj)
#
#
# class Cart(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
#     books = models.ManyToManyField(BookList, blank=True)
#     sub_total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
#     total = models.DecimalField(default=0.00, decimal_places=2, max_digits=9)
#     timestamp = models.DateTimeField(auto_now_add=True)
#     update = models.DateTimeField(auto_now=True)
#
#     objects = CartManager()
#
#     def __str__(self):
#         return str(self.id)
#
#     def get_vat(self):
#         vat = format(Decimal(self.sub_total) * Decimal(1.10) - Decimal(self.sub_total), '.2f')
#         return vat
#
#
# def m2m_save_cart_receiver(sender, instance, action, *args, **kwargs):
#     if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
#         products = instance.books.all()
#         subtotal = 0
#         for x in products:
#             subtotal += x.price
#         instance.sub_total = subtotal
#         instance.save()
#         # for book in products:
#         #     book_id = book.id
#         #     print(book_id)
#         #     book = BookList.objects.get_by_id(book_id)
#         #     print(book.order)
#         #     book.order += 1
#         #     book.save()
#
#
# m2m_changed.connect(m2m_save_cart_receiver, sender=Cart.books.through)
#
#
# # def pre_save_items_receiver(sender, instance, *args, **kwargs):
# #     instance.price = instance.book.price
# #     instance.total = instance.price * instance.quantity
# #
# #
# # pre_save.connect(pre_save_items_receiver, sender=Items)
#
#
# def pre_save_cart_receiver(sender, instance, *args, **kwargs):
#     if instance.sub_total > 0:
#         instance.total = Decimal(instance.sub_total) * Decimal(1.10)
#     else:
#         instance.total = 0.00
#
#
# pre_save.connect(pre_save_cart_receiver, sender=Cart)
