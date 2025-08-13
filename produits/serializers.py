from rest_framework import serializers
from .models import (
    Category, Brand, Product, ProductVariant, SpecCategory,
    SpecKey, ProductSpecification, ProductImage, ProductDocument,
    RelatedProduct, Warehouse, StockLevel, StockMovement
)

# --- Serializers de base ---

class CategorySerializer(serializers.ModelSerializer):
    subcategories = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'nom', 'parent_category', 'subcategories', 'description']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'nom', 'logo', 'description']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'product', 'nom', 'valeur', 'prix_supplémentaire', 'stock', 'image']


class SpecCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecCategory
        fields = ['id', 'nom', 'description']


class SpecKeySerializer(serializers.ModelSerializer):
    spec_category = SpecCategorySerializer(read_only=True)
    spec_category_id = serializers.PrimaryKeyRelatedField(
        queryset=SpecCategory.objects.all(),
        source='spec_category',
        write_only=True
    )

    class Meta:
        model = SpecKey
        fields = [
            'id', 'spec_category', 'spec_category_id', 'nom_attribut',
            'data_type', 'unit', 'is_filterable', 'position', 'description'
        ]


class ProductSpecificationSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    spec_key = SpecKeySerializer(read_only=True)
    spec_key_id = serializers.PrimaryKeyRelatedField(
        queryset=SpecKey.objects.all(),
        source='spec_key',
        write_only=True
    )

    class Meta:
        model = ProductSpecification
        fields = ['id', 'product', 'spec_key', 'spec_key_id', 'valeur']


from rest_framework import serializers
from .models import ProductImage, Product

class ProductImageSerializer(serializers.ModelSerializer):
    # product : affichage du produit dans la réponse (read_only)
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    # product_id : écriture via le champ product, attend un ID valide
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True,
    )

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'product_id', 'image', 'alt_text']

    def validate(self, data):
        # Validation optionnelle : s'assurer qu'une image est envoyée
        if not data.get('image'):
            raise serializers.ValidationError({"image": "Un fichier image est requis."})
        return data


class ProductDocumentSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )

    class Meta:
        model = ProductDocument
        fields = ['id', 'product', 'product_id', 'url_document', 'type_document']


# --- Serializer simplifié pour éviter la dépendance circulaire ---

class ProductBriefSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'nom', 'ean_code']


# --- RelatedProductSerializer utilisant ProductBriefSerializer ---

class RelatedProductSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    related_product = ProductBriefSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    related_product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='related_product',
        write_only=True
    )

    class Meta:
        model = RelatedProduct
        fields = ['id', 'product', 'product_id', 'related_product', 'related_product_id', 'relation_type']


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'nom', 'adresse', 'code_postal', 'ville', 'pays', 'type', 'is_active', 'commentaire']


class StockLevelSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='warehouse',
        write_only=True
    )
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        source='variant',
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = StockLevel
        fields = [
            'id', 'warehouse', 'warehouse_id', 'product', 'product_id',
            'variant', 'variant_id', 'stock_total', 'stock_reserve', 'seuil_alerte'
        ]


class StockMovementSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='warehouse',
        write_only=True
    )
    product = serializers.PrimaryKeyRelatedField(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        write_only=True
    )
    variant = ProductVariantSerializer(read_only=True)
    variant_id = serializers.PrimaryKeyRelatedField(
        queryset=ProductVariant.objects.all(),
        source='variant',
        write_only=True,
        allow_null=True,
        required=False
    )
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = StockMovement
        fields = [
            'id', 'warehouse', 'warehouse_id', 'product', 'product_id',
            'variant', 'variant_id', 'mouvement_type', 'quantite',
            'date_mouvement', 'commentaire', 'user'
        ]


# --- ProductSerializer enrichi avec toutes les relations ---

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(),
        source='brand',
        write_only=True
    )
    variants = ProductVariantSerializer(many=True, read_only=True)

    # Relations enrichies en lecture seule
    specifications = ProductSpecificationSerializer(
    many=True,
    read_only=True, 
     # ou nom correct du related_name dans vos modèles
)
    related_products = RelatedProductSerializer(many=True, read_only=True, source='related_from')

    stock_levels = StockLevelSerializer(many=True, read_only=True, source='stocklevel_set')
    images = ProductImageSerializer(many=True, read_only=True)
    documents = ProductDocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_id', 'brand', 'brand_id', 'nom', 'description',
            'prix', 'stock', 'etat', 'image', 'ean_code', 'is_active',
            'date_creation', 'date_modification', 'variants',
            'specifications', 'related_products', 'stock_levels', 'images', 'documents'
        ]
