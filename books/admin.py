from django.contrib import admin
from .models import Books


# Register your models here.
@admin.register(Books)
class BooksAdmin(admin.ModelAdmin):
    fields_list = ["title", "author", "published_date", "isbn", "pages"]
