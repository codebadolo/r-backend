from rest_framework import serializers
from .models import (
    Brand, Category, ProductType, ProductAttribute, ProductAttributeValue, ProductTypeAttribute, Product,
    ProductInventory, ProductAttributeValues, Media, Stock, SectionSpecification, CleSpecification,
    ProduitSpecification
)


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['id', 'name', 'logo']
        read_only_fields = ['id']


class CategorySerializer(serializers.ModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'is_active']
        read_only_fields = ['id', 'slug']


class ProductTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductType
        fields = ['id', 'name']
        read_only_fields = ['id']



class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class ProductAttributeValueSerializer(serializers.ModelSerializer):
    product_attribute = serializers.PrimaryKeyRelatedField(queryset=ProductAttribute.objects.all())

    class Meta:
        model = ProductAttributeValue
        fields = ['id', 'product_attribute', 'value']
        read_only_fields = ['id']


class ProductTypeAttributeSerializer(serializers.ModelSerializer):
    product_attribute = ProductAttributeSerializer(read_only=True)
    product_attribute_id = serializers.PrimaryKeyRelatedField(
        source='product_attribute',
        queryset=ProductAttribute.objects.all(),
        write_only=True
    )

    class Meta:
        model = ProductTypeAttribute
        fields = ['id', 'product_type', 'product_attribute', 'product_attribute_id']
        read_only_fields = ['id']


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Media
        fields = ['id', 'product_inventory', 'img_url', 'alt_text', 'is_feature', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['id', 'product_inventory', 'last_checked', 'units', 'units_sold']
        read_only_fields = ['id', 'last_checked']


class ProductAttributeValuesSerializer(serializers.ModelSerializer):
    product_attribute_value = serializers.PrimaryKeyRelatedField(queryset=ProductAttributeValue.objects.all())
    product_inventory = serializers.PrimaryKeyRelatedField(read_only=True)  # assigné automatiquement

    class Meta:
        model = ProductAttributeValues
        fields = ['product_attribute_value', 'product_inventory']


class ProductInventorySerializer(serializers.ModelSerializer):
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    product_type = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all())
    product = serializers.PrimaryKeyRelatedField(read_only=True)  # assigné automatiquement
    
    attributes = ProductAttributeValuesSerializer(
        many=True, required=False, source='attribute_values'
    )
    media = MediaSerializer(many=True, read_only=True)
    stock = StockSerializer(read_only=True)

    class Meta:
        model = ProductInventory
        fields = [
            'id', 'sku', 'upc', 'product_type', 'product', 'brand', 'attributes', 'is_active',
            'is_default', 'retail_price', 'store_price', 'is_digital', 'weight',
            'media', 'stock', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'product', 'created_at', 'updated_at']

    def create(self, validated_data):
        attributes_data = validated_data.pop('attribute_values', [])
        inventory = ProductInventory.objects.create(**validated_data)

        for attr_val in attributes_data:
            ProductAttributeValues.objects.create(
                product_inventory=inventory,
                product_attribute_value=attr_val['product_attribute_value']
            )
        return inventory

    def update(self, instance, validated_data):
        attributes_data = validated_data.pop('attribute_values', None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if attributes_data is not None:
            instance.attribute_values.all().delete()
            for attr_val in attributes_data:
                ProductAttributeValues.objects.create(
                    product_inventory=instance,
                    product_attribute_value=attr_val['product_attribute_value']
                )
        return instance


class ProduitSpecificationSerializer(serializers.ModelSerializer):
    cle_specification = serializers.PrimaryKeyRelatedField(queryset=CleSpecification.objects.all())
    product = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ProduitSpecification
        fields = ['cle_specification', 'value', 'product']


class CleSpecificationSerializer(serializers.ModelSerializer):
    section = serializers.PrimaryKeyRelatedField(queryset=SectionSpecification.objects.all())

    class Meta:
        model = CleSpecification
        fields = ['id', 'name', 'section', 'order']
        read_only_fields = ['id']


class SectionSpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SectionSpecification
        fields = ['id', 'name', 'order']
        read_only_fields = ['id']


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.filter(is_active=True))
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all())
    product_type = serializers.PrimaryKeyRelatedField(queryset=ProductType.objects.all())

    inventories = ProductInventorySerializer(many=True, required=False)
    specifications = ProduitSpecificationSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'id', 'web_id', 'slug', 'name', 'description', 'category', 'brand', 'product_type', 'is_active',
            'inventories', 'specifications', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def create(self, validated_data):
        inventories_data = validated_data.pop('inventories', [])
        specifications_data = validated_data.pop('specifications', [])

        product = Product.objects.create(**validated_data)

        for inventory_data in inventories_data:
            attr_data = inventory_data.pop('attribute_values', [])
            stock_data = inventory_data.pop('stock', None)
            inventory = ProductInventory.objects.create(product=product, **inventory_data)
            for attr in attr_data:
                ProductAttributeValues.objects.create(product_inventory=inventory, **attr)
            if stock_data:
                Stock.objects.create(product_inventory=inventory, **stock_data)

        for spec_data in specifications_data:
            ProduitSpecification.objects.create(product=product, **spec_data)

        return product

    def update(self, instance, validated_data):
        inventories_data = validated_data.pop('inventories', None)
        specifications_data = validated_data.pop('specifications', None)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()

        if inventories_data is not None:
            instance.inventories.all().delete()
            for inventory_data in inventories_data:
                attr_data = inventory_data.pop('attribute_values', [])
                stock_data = inventory_data.pop('stock', None)
                inventory = ProductInventory.objects.create(product=instance, **inventory_data)
                for attr in attr_data:
                    ProductAttributeValues.objects.create(product_inventory=inventory, **attr)
                if stock_data:
                    Stock.objects.create(product_inventory=inventory, **stock_data)

        if specifications_data is not None:
            instance.specifications.all().delete()
            for spec_data in specifications_data:
                ProduitSpecification.objects.create(product=instance, **spec_data)

        return instance
