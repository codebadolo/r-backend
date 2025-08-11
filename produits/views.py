from rest_framework import viewsets
from .models import (
    Category, Brand, Product, ProductVariant, SpecCategory,
    SpecKey, ProductSpecification, ProductImage, ProductDocument,
    RelatedProduct, Warehouse, StockLevel, StockMovement
)
from rest_framework import viewsets, generics, status, permissions
from .serializers import (
    CategorySerializer, BrandSerializer, ProductSerializer, ProductVariantSerializer,
    SpecCategorySerializer, SpecKeySerializer, ProductSpecificationSerializer,
    ProductImageSerializer, ProductDocumentSerializer, RelatedProductSerializer,
    WarehouseSerializer, StockLevelSerializer, StockMovementSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all()
    serializer_class = ProductVariantSerializer


class SpecCategoryViewSet(viewsets.ModelViewSet):
    queryset = SpecCategory.objects.all()
    serializer_class = SpecCategorySerializer


class SpecKeyViewSet(viewsets.ModelViewSet):
    queryset = SpecKey.objects.all()
    serializer_class = SpecKeySerializer


class ProductSpecificationViewSet(viewsets.ModelViewSet):
    queryset = ProductSpecification.objects.all()
    serializer_class = ProductSpecificationSerializer


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class ProductDocumentViewSet(viewsets.ModelViewSet):
    queryset = ProductDocument.objects.all()
    serializer_class = ProductDocumentSerializer


class RelatedProductViewSet(viewsets.ModelViewSet):
    queryset = RelatedProduct.objects.all()
    serializer_class = RelatedProductSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class StockLevelViewSet(viewsets.ModelViewSet):
    queryset = StockLevel.objects.all()
    serializer_class = StockLevelSerializer


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
