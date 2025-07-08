# admin.py
from django.contrib import admin
from .models import (
    Genre, Series, Maker, Actress, Director,
    Author, Label, Product
)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'content_id', 'product_id', 'release_date')
    search_fields = ('title', 'content_id', 'product_id')

admin.site.register(Genre)
admin.site.register(Series)
admin.site.register(Maker)
admin.site.register(Actress)
admin.site.register(Director)
admin.site.register(Author)
admin.site.register(Label)
admin.site.register(Product, ProductAdmin)
