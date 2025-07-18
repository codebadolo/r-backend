from rest_framework import generics
from .models import (
    Category, Brand, ProductType, Product,
    ProductAttribute, ProductAttributeValue,
    ProductImage, Stock, Warehouse, ProductAttributeOption
)
from .serializers import (
    CategorySerializer,
    BrandSerializer,
    ProductTypeSerializer,
    ProductSerializer,
    ProductDetailSerializer ,
    ProductAttributeSerializer,
    ProductAttributeValueReadSerializer,
    ProductAttributeValueWriteSerializer,
    ProductImageSerializer,
    StockSerializer,
    WarehouseSerializer,
    ProductCreateUpdateSerializer,
    ProductAttributeOptionSerializer
)
from rest_framework.parsers import MultiPartParser, FormParser

# CATEGORY
class CategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# BRAND
class BrandListCreateAPIView(generics.ListCreateAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class BrandRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


# PRODUCT TYPE
class ProductTypeListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


class ProductTypeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductType.objects.all()
    serializer_class = ProductTypeSerializer


# PRODUCT ATTRIBUTE
class ProductAttributeListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


class ProductAttributeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttribute.objects.all()
    serializer_class = ProductAttributeSerializer


# PRODUCT ATTRIBUTE VALUE
class ProductAttributeValueListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductAttributeValue.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return ProductAttributeValueWriteSerializer
        return ProductAttributeValueReadSerializer


class ProductAttributeValueRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttributeValue.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductAttributeValueWriteSerializer
        return ProductAttributeValueReadSerializer


# PRODUCT ATTRIBUTE OPTION
from django_filters.rest_framework import DjangoFilterBackend

class ProductAttributeOptionListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductAttributeOption.objects.all()
    serializer_class = ProductAttributeOptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['attribute']  # Permet de filtrer par ?attribute=ID



class ProductAttributeOptionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductAttributeOption.objects.all()
    serializer_class = ProductAttributeOptionSerializer


# PRODUCT IMAGE
class ProductImageListCreateAPIView(generics.ListCreateAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]


class ProductImageRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    parser_classes = [MultiPartParser, FormParser]


# WAREHOUSE
class WarehouseListCreateAPIView(generics.ListCreateAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


class WarehouseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


# STOCK
class StockListCreateAPIView(generics.ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


class StockRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer


# # PRODUCT
# class ProductListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


# class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer  # GET list utilise lecture enrichie


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductCreateUpdateSerializer
        return ProductDetailSerializer  # GET détail utilise lecture enrichie
