from rest_framework import serializers
from .models import (
    Brand, Category, ProductType, ProductAttribute, ProductAttributeValue,
    ProductTypeAttribute, Product, ProductInventory, ProductAttributeValues,
    Media, Stock, SectionSpecification, CleSpecification, ProduitSpecification
)

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = '__all__'

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = '__all__'

class ProductAttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValue
        fields = '__all__'

class ProductTypeAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductTypeAttribute
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductInventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductInventory
        fields = '__all__'

class ProductAttributeValuesSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttributeValues
        fields = '__all__'

class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = '__all__'

class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'

class SectionSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionSpecification
        fields = '__all__'

class CleSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CleSpecification
        fields = '__all__'

class ProduitSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProduitSpecification
        fields = '__all__'
