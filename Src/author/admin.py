from django.contrib import admin
from .models import BookAuthor


# Register your models here.

class BookAuthorAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'bio']
    search_fields = ['name', 'bio']
    # filter_vertical = ['category__mainCat__name']
    list_per_page = 15
    list_filter = ['name']

    class Meta:
        Model = BookAuthor


admin.site.register(BookAuthor, BookAuthorAdmin)
