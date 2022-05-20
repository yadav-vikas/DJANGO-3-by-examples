from django.contrib import admin
from .models import Product, Category,ExtraItemOptions, ItemOptions

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated',]
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ExtraItemOptions)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Product_name_extra_item_options', 'option_name_extra_item_options','price_extra_item_options']

@admin.register(ItemOptions)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['Product_name_item_options', 'option_name_item_options','price_item_options']
    