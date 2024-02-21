from django.contrib import admin
from .models import Product,Cart,ProductReport

class ProductAdmin(admin.ModelAdmin):
    list_display = ['product_id', 'brand', 'name', 'category', 'product_type', 'price', 'food_additives', 'food_preservatives', 'image', 'image_id', 'is_approved']
    search_fields = ['name', 'category', 'product_type']
    list_filter = ['brand', 'category', 'product_type', 'is_approved']

admin.site.register(Product, ProductAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'quantity']
    search_fields = ['user__username', 'product__name']
    list_filter = ['user', 'product']

admin.site.register(Cart, CartAdmin)

class ProductReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'active']
    list_filter = ['user', 'product', 'active']
    search_fields = ['user__username', 'product__name']

admin.site.register(ProductReport, ProductReportAdmin)
