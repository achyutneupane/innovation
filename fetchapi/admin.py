from django.contrib import admin
from . import models
# Register your models here.

@admin.register(models.Products)
class Products(admin.ModelAdmin):
    list_display = ['petroleum_product']
