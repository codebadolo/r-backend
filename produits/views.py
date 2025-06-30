from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
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
    permission_classes = [IsAuthenticated]
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
class ProductTypeViewSet(viewsets.ModelViewSet):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer
    permission_classes = [IsAuthenticated]
class ProductAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer
    permission_classes = [IsAuthenticated]
class ProductAttributeValueViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValue.objects.all()
    serializer_class = ProductAttributeValueSerializer
    permission_classes = [IsAuthenticated]
class ProductTypeAttributeViewSet(viewsets.ModelViewSet):
    queryset = ProductTypeAttribute.objects.all()
    serializer_class = ProductTypeAttributeSerializer
    permission_classes = [IsAuthenticated]
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
class ProductInventoryViewSet(viewsets.ModelViewSet):
    queryset = ProductInventory.objects.all()
    serializer_class = ProductInventorySerializer
    permission_classes = [IsAuthenticated]
class ProductAttributeValuesViewSet(viewsets.ModelViewSet):
    queryset = ProductAttributeValues.objects.all()
    serializer_class = ProductAttributeValuesSerializer
    permission_classes = [IsAuthenticated]
class MediaViewSet(viewsets.ModelViewSet):
    queryset = Media.objects.all()
    serializer_class = MediaSerializer
    permission_classes = [IsAuthenticated]
class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]
class SectionSpecificationViewSet(viewsets.ModelViewSet):
    queryset = SectionSpecification.objects.all()
    serializer_class = SectionSpecificationSerializer
    permission_classes = [IsAuthenticated]
class CleSpecificationViewSet(viewsets.ModelViewSet):
    queryset = CleSpecification.objects.all()
    serializer_class = CleSpecificationSerializer
    permission_classes = [IsAuthenticated]
class ProduitSpecificationViewSet(viewsets.ModelViewSet):
    queryset = ProduitSpecification.objects.all()
    serializer_class = ProduitSpecificationSerializer
    permission_classes = [IsAuthenticated]