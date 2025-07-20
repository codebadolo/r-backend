from rest_framework import serializers
from .models import (
    Category, Brand, ProductType, Product,
    ProductAttribute, ProductAttributeValue,
    ProductAttributeOption, ProductImage, Stock, Warehouse
)

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'location']

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'parent']

class BrandSerializer(serializers.ModelSerializer):
    logo = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']

    def get_logo(self, obj):
        request = self.context.get('request')
        if obj.logo and hasattr(obj.logo, 'url'):
            return request.build_absolute_uri(obj.logo.url)
        return None


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'product_type']


'''class ProductAttributeOptionSerializer(serializers.ModelSerializer):
    attribute = serializers.PrimaryKeyRelatedField(
        queryset=ProductAttribute.objects.all()
    )

    class Meta:
        model = ProductAttributeOption
        fields = ['id', 'attribute', 'value']'''
class ProductAttributeOptionSerializer(serializers.ModelSerializer):
    attribute = ProductAttributeSerializer(read_only=True)  # << imbriqué ici

    class Meta:
        model = ProductAttributeOption
        fields = ['id', 'value', 'attribute']


# # Serializer d’écriture de ProductAttributeValue (pour POST/PUT/PATCH)
# class ProductAttributeValueWriteSerializer(serializers.ModelSerializer):
#     option = serializers.PrimaryKeyRelatedField(queryset=ProductAttributeOption.objects.all())
#     product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

#     class Meta:
#         model = ProductAttributeValue
#         fields = ['id', 'product', 'option']

class ProductAttributeValueWriteSerializer(serializers.ModelSerializer):
    option = serializers.PrimaryKeyRelatedField(
        queryset=ProductAttributeOption.objects.all()
    )
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'product', 'option']


# Serializer de lecture détaillée (pour GET), imbriquant option et attribut
class ProductAttributeValueReadSerializer(serializers.ModelSerializer):
    option = ProductAttributeOptionSerializer(read_only=True)
    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'product', 'option']
class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()

    class Meta:
        model = ProductImage
        fields = ['id', 'product', 'image', 'is_feature', 'alt_text']
        extra_kwargs = {
            'product': {'required': True},
            'image': {'required': True},
        }

'''class StockSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)
    warehouse_id = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(),
        source='warehouse',
        write_only=True,
        required=True
    )

    class Meta:
        model = Stock
        fields = ['id', 'product', 'warehouse', 'warehouse_id', 'units_sold']'''

class StockSerializer(serializers.ModelSerializer):
    warehouse = WarehouseSerializer(read_only=True)

    class Meta:
        model = Stock
        fields = ['id', 'product', 'warehouse', 'warehouse_id', 'units', 'units_sold']
class ProductDetailSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    product_type = ProductTypeSerializer(read_only=True)
    attribute_values = ProductAttributeValueReadSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stocks = StockSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
        
class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source='brand')
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')
    product_type_id = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all(), source='product_type')

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category_id', 'brand_id', 'product_type_id',
            'description', 'price', 'is_active',
        ]
        
# Serializer principal produit
class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    brand_id = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), source='brand', write_only=True)

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category', write_only=True)

    product_type = ProductTypeSerializer(read_only=True)
    product_type_id = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all(), source='product_type', write_only=True)

    attribute_values = ProductAttributeValueReadSerializer(many=True, read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    stocks = StockSerializer(many=True, read_only=True, source='stock_set')  # <-- Ajout important

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'category', 'category_id',
            'brand', 'brand_id', 'product_type', 'product_type_id',
            'description', 'price', 'is_active',
            'created_at', 'updated_at',
            'attribute_values', 'images', 'stocks'
        ]

