from rest_framework import serializers
from .models import (
    Category, Brand, Product, ProductVariant, SpecCategory,
    SpecKey, ProductSpecification, ProductImage, ProductDocument,
    RelatedProduct, Warehouse, StockLevel, StockMovement
)

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'nom', 'parent_category', 'subcategories', 'description']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'nom', 'logo_url', 'description']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'nom', 'valeur', 'prix_supplémentaire', 'stock', 'image_url']


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source='brand', write_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_id', 'brand', 'brand_id', 'nom', 'description',
            'prix', 'stock', 'etat', 'image_url', 'ean_code', 'is_active',
            'date_creation', 'date_modification', 'variants'
        ]


class SpecCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecCategory
        fields = ['id', 'nom', 'description']


class SpecKeySerializer(serializers.ModelSerializer):
    spec_category = SpecCategorySerializer(read_only=True)
    spec_category_id = serializers.PrimaryKeyRelatedField(queryset=SpecCategory.objects.all(), source='spec_category', write_only=True)

    class Meta:
        model = SpecKey
        fields = ['id', 'spec_category', 'spec_category_id', 'nom_attribut', 'data_type', 'unit', 'is_filterable', 'position', 'description']


class ProductSpecificationSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    spec_key = SpecKeySerializer(read_only=True)
    spec_key_id = serializers.PrimaryKeyRelatedField(queryset=SpecKey.objects.all(), source='spec_key', write_only=True)

    class Meta:
        model = ProductSpecification
        fields = ['id', 'product', 'product_id', 'spec_key', 'spec_key_id', 'valeur']


class ProductImageSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'product_id', 'image_url', 'alt_text']


class ProductDocumentSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)

    class Meta:
        model = ProductDocument
        fields = ['id', 'product', 'product_id', 'url_document', 'type_document']


class RelatedProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    related_product = ProductSerializer(read_only=True)
    related_product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='related_product', write_only=True)

    class Meta:
        model = RelatedProduct
        fields = ['id', 'product', 'product_id', 'related_product', 'related_product_id', 'relation_type']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'nom', 'adresse', 'code_postal', 'ville', 'pays', 'type', 'is_active', 'commentaire']


class StockLevelSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), source='warehouse', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='variant', write_only=True, allow_null=True, required=False)

    class Meta:
        model = StockLevel
        fields = ['id', 'warehouse', 'warehouse_id', 'product', 'product_id', 'variant', 'variant_id', 'stock_total', 'stock_reserve', 'seuil_alerte']


class StockMovementSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(queryset=Warehouse.objects.all(), source='warehouse', write_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), source='product', write_only=True)
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(queryset=ProductVariant.objects.all(), source='variant', write_only=True, allow_null=True, required=False)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StockMovement
        fields = ['id', 'warehouse', 'warehouse_id', 'product', 'product_id', 'variant', 'variant_id', 'mouvement_type', 'quantite', 'date_mouvement', 'commentaire', 'user']
