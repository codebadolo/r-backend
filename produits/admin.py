# produits/admin.py

from django.contrib import admin
from .models import (
    Category, Brand, ProductType, Product,
    ProductAttribute, ProductAttributeValue,
    ProductImage, Stock, Warehouse
)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'category', 'product_type', 'price', 'is_active', 'created_at']
    list_filter = ['brand', 'category', 'product_type', 'is_active']
    search_fields = ['name', 'description']
    inlines = []

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(ProductType)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValue)
admin.site.register(ProductImage)
admin.site.register(Stock)
admin.site.register(Warehouse)
