from django.contrib import admin
from product.models import (
     BookList,
)

# Register your models here.


class BookListAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'price', 'get_rent_charge', 'get_discount',
                    'timestamp', 'active', 'is_old', 'is_stock', 'is_rent_available', 'slug']
    search_fields = ['descriptions', 'name', 'author__name']
    filter_vertical = ['tag']
    list_per_page = 25
    list_filter = ['author', 'price', 'category', 'is_stock', 'active', 'timestamp']

    class Meta:
        Model = BookList


admin.site.register(BookList, BookListAdmin)


