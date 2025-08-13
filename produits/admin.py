from django.contrib import admin
from django.utils.html import format_html

from .models import (
    Category, Brand, Product, ProductVariant,
    SpecCategory, SpecKey, ProductSpecification,
    ProductImage, ProductDocument, RelatedProduct,
    Warehouse, StockLevel, StockMovement
)


# --- Category ---
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'parent_category', 'description')
    search_fields = ('nom', 'description')
    list_filter = ('parent_category',)
    ordering = ('nom',)

admin.site.register(Category, CategoryAdmin)


# --- Brand ---
class BrandAdmin(admin.ModelAdmin):
    list_display = ('nom', 'logo_preview', 'description')
    search_fields = ('nom', 'description')

    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height: 40px;"/>', obj.logo)
        return "-"
    logo_preview.short_description = 'Logo'

admin.site.register(Brand, BrandAdmin)


# --- ProductVariant inline (pour Product) ---
class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1
    fields = ('nom', 'valeur', 'prix_supplémentaire', 'stock', 'image')
    readonly_fields = ()
    show_change_link = True


# --- ProductSpecification inline (pour Product) ---
class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1
    fields = ('spec_key', 'valeur')
    autocomplete_fields = ('spec_key',)
    show_change_link = True


# --- ProductImage inline (pour Product) ---
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text')
    show_change_link = False


# --- ProductDocument inline (pour Product) ---
class ProductDocumentInline(admin.TabularInline):
    model = ProductDocument
    extra = 1
    fields = ('url_document', 'type_document')
    show_change_link = False


# --- ProductAdmin ---
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('nom', 'category', 'brand', 'prix', 'stock', 'etat', 'is_active', 'date_creation', 'date_modification')
    list_filter = ('category', 'brand', 'etat', 'is_active')
    search_fields = ('nom', 'description', 'ean_code')
    readonly_fields = ('date_creation', 'date_modification')
    autocomplete_fields = ('category', 'brand')
    inlines = (ProductVariantInline, ProductSpecificationInline, ProductImageInline, ProductDocumentInline)
    ordering = ('nom',)
    fieldsets = (
        (None, {
            'fields': ('nom', 'category', 'brand', 'description', 'prix', 'stock', 'etat', 'image', 'ean_code', 'is_active')
        }),
        ('Dates', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',),
        }),
    )


# --- SpecCategoryAdmin ---
@admin.register(SpecCategory)
class SpecCategoryAdmin(admin.ModelAdmin):
    list_display = ('nom', 'description')
    search_fields = ('nom', 'description')


# --- SpecKeyAdmin ---
@admin.register(SpecKey)
class SpecKeyAdmin(admin.ModelAdmin):
    list_display = ('nom_attribut', 'spec_category', 'data_type', 'unit', 'is_filterable', 'position')
    list_editable = ('position', 'is_filterable')
    list_filter = ('spec_category', 'data_type')
    search_fields = ('nom_attribut', 'description')
    autocomplete_fields = ('spec_category',)
    ordering = ('position',)


# --- WarehouseAdmin ---
@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'ville', 'pays', 'type', 'is_active')
    list_filter = ('type', 'is_active', 'pays')
    search_fields = ('nom', 'adresse', 'ville', 'code_postal')


# --- StockLevelAdmin ---
@admin.register(StockLevel)
class StockLevelAdmin(admin.ModelAdmin):
    list_display = ('warehouse', 'product', 'variant', 'stock_total', 'stock_reserve', 'seuil_alerte')
    list_filter = ('warehouse', 'product')
    search_fields = ('product__nom', 'variant__nom')
    #autocomplete_fields = ('warehouse', 'product', 'variant')
    ordering = ('warehouse', 'product')


# --- StockMovementAdmin ---
@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'variant', 'warehouse', 'mouvement_type', 'quantite', 'date_mouvement', 'user')
    list_filter = ('mouvement_type', 'warehouse', 'date_mouvement')
    search_fields = ('product__nom', 'variant__nom', 'user__username')
    #autocomplete_fields = ('warehouse', 'product', 'variant', 'user')
    date_hierarchy = 'date_mouvement'


# --- RelatedProductAdmin ---
@admin.register(RelatedProduct)
class RelatedProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'related_product', 'relation_type')
    search_fields = ('product__nom', 'related_product__nom', 'relation_type')
    autocomplete_fields = ('product', 'related_product')

admin.site.register(ProductImage)