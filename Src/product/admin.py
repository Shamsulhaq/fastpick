from django.contrib import admin
from .models import (
    BookAuthor, BookList,
    Category, Tag
)


# Register your models here.

class BookListAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'category', 'price', 'get_rent_charge','get_discount', 'is_stock']
    # search_fields = ['descriptions', 'tag']
    # filter_vertical = ['category__mainCat__name']
    list_per_page = 15
    list_filter = ['author', 'category', 'is_stock']

    class Meta:
        Model = BookList


admin.site.register(BookList, BookListAdmin)


class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'bio']
    search_fields = ['name', 'bio']
    # filter_vertical = ['category__mainCat__name']
    list_per_page = 15
    list_filter = ['name']

    class Meta:
        Model = BookAuthor


admin.site.register(BookAuthor, BookAuthorAdmin)
admin.site.register(Category)
admin.site.register(Tag)
