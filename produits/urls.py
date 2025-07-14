from rest_framework.routers import DefaultRouter
from .views import (
    BrandViewSet, CategoryViewSet, ProductTypeViewSet, ProductAttributeViewSet,
    ProductAttributeValueViewSet, ProductTypeAttributeViewSet, ProductViewSet,
    ProductInventoryViewSet, ProductAttributeValuesViewSet, MediaViewSet,
    StockViewSet, SectionSpecificationViewSet, CleSpecificationViewSet,
    ProduitSpecificationViewSet
)
from rest_framework.generics import RetrieveAPIView
from .views import ProductDetailBySlugView
from django.urls import path ,include
router = DefaultRouter()
router.register(r'brands', BrandViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'product-types', ProductTypeViewSet)
router.register(r'product-attributes', ProductAttributeViewSet)
router.register(r'product-attribute-values', ProductAttributeValueViewSet)
router.register(r'product-type-attributes', ProductTypeAttributeViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-inventories', ProductInventoryViewSet)
router.register(r'product-attribute-values-links', ProductAttributeValuesViewSet)
router.register(r'media', MediaViewSet)
router.register(r'stocks', StockViewSet)
router.register(r'section-specifications', SectionSpecificationViewSet)
router.register(r'cle-specifications', CleSpecificationViewSet)
router.register(r'produit-specifications', ProduitSpecificationViewSet)


urlpatterns = router.urls
