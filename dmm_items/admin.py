# admin.py
from django.contrib import admin
from .models import (
    Genre, Series, Maker, Actress, Director,
    Author, Label, Product
)

admin.site.register(Genre)
admin.site.register(Series)
admin.site.register(Maker)
admin.site.register(Actress)
admin.site.register(Director)
admin.site.register(Author)
admin.site.register(Label)
admin.site.register(Product)
