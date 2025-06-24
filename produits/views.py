from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from .models import (
    Brand, Category, ProductType, ProductAttribute, ProductAttributeValue,
    ProductTypeAttribute, Product, ProductInventory, ProductAttributeValues,
    Media, Stock, SectionSpecification, CleSpecification, ProduitSpecification
)
from .serializers import (
    BrandSerializer, CategorySerializer, ProductTypeSerializer, ProductAttributeSerializer,
    ProductAttributeValueSerializer, ProductTypeAttributeSerializer, ProductSerializer,
    ProductInventorySerializer, ProductAttributeValuesSerializer, MediaSerializer,
    StockSerializer, SectionSpecificationSerializer, CleSpecificationSerializer,
    ProduitSpecificationSerializer
)

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer

class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer

class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer

class ProductTypeAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductTypeAttribute.objects.all()
    serializer_class = ProductTypeAttributeSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer

class ProductAttributeValuesViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValues.objects.all()
    serializer_class = ProductAttributeValuesSerializer

class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

class SectionSpecificationViewSet(viewsets.ModelViewSet):
    queryset = SectionSpecification.objects.all()
    serializer_class = SectionSpecificationSerializer

class CleSpecificationViewSet(viewsets.ModelViewSet):
    queryset = CleSpecification.objects.all()
    serializer_class = CleSpecificationSerializer

class ProduitSpecificationViewSet(viewsets.ModelViewSet):
    queryset = ProduitSpecification.objects.all()
    serializer_class = ProduitSpecificationSerializer
