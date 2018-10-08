from django.contrib import admin
from product.models import (
    BookAuthor, BookList,
)

# Register your models here.


class BookListAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'price', 'get_rent_charge', 'get_discount',
                    'timeStamp', 'active', 'is_old', 'is_stock', 'is_rent_available', 'slug']
    search_fields = ['descriptions', 'name', 'author__name']
    filter_vertical = ['tag']
    list_per_page = 15
    list_filter = ['author', 'price', 'category', 'is_stock', 'active', 'timeStamp']

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
