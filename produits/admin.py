from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category, Brand, ProductType, Product, ProductImage,
    ProductAttribute, ProductAttributeOption, ProductAttributeValue,
    Warehouse, Stock
)
from unfold.admin import ModelAdmin ,TabularInline


admin.site.register(Category)
admin.site.register(Brand)

admin.site.register(ProductImage)


# Enregistrement admin du modèle ProductAttributeOption nécessaire pour autocomplete_fields
@admin.register(ProductAttributeOption)
class ProductAttributeOptionAdmin(ModelAdmin):
    list_display = ('attribute', 'value')
    search_fields = ('value', 'attribute__name')
    list_filter = ('attribute',)

class ProductAttributeOptionInline(TabularInline):
    model = ProductAttributeOption
    extra = 1

@admin.register(ProductAttribute)
class ProductAttributeAdmin(ModelAdmin):
    list_display = ('name', 'product_type')
    search_fields = ('name',)
    list_filter = ('product_type',)
    inlines = [ProductAttributeOptionInline]

class ProductAttributeValueInline(TabularInline):
    model = ProductAttributeValue
    extra = 1
    autocomplete_fields = ['option']

class ProductImageInline(TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:60px;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Aperçu'

class StockInline(TabularInline):
    model = Stock
    extra = 1
    fields = ('warehouse', 'units', 'units_sold')
    autocomplete_fields = ['warehouse']

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'category', 'brand', 'product_type', 'price', 'stock_summary', 'is_active')
    list_filter = ('category', 'brand', 'product_type', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    inlines = [ProductImageInline, ProductAttributeValueInline, StockInline]

    def stock_summary(self, obj):
        stocks = obj.stock_set.all()
        if not stocks.exists():
            return "-"
        total_units = sum(stock.units for stock in stocks)
        per_warehouse = ", ".join(f"{stock.warehouse.name}: {stock.units}" for stock in stocks)
        return format_html(
            "<strong>{}</strong> unités<br/><small>{}</small>",
            total_units,
            per_warehouse
        )
    stock_summary.short_description = "Stock par entrepôt"
    stock_summary.allow_tags = True

@admin.register(Warehouse)
class WarehouseAdmin(ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Stock)
class StockAdmin(ModelAdmin):
    list_display = ('product', 'warehouse', 'units', 'units_sold')
    list_filter = ('warehouse',)
    search_fields = ('product__name',)
    autocomplete_fields = ['product', 'warehouse']
