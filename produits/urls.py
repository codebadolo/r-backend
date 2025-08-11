from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CategoryViewSet, BrandViewSet, ProductViewSet, ProductVariantViewSet,
    SpecCategoryViewSet, SpecKeyViewSet, ProductSpecificationViewSet,
    ProductImageViewSet, ProductDocumentViewSet, RelatedProductViewSet,
    WarehouseViewSet, StockLevelViewSet, StockMovementViewSet
)

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'brands', BrandViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-variants', ProductVariantViewSet)
router.register(r'spec-categories', SpecCategoryViewSet)
router.register(r'spec-keys', SpecKeyViewSet)
router.register(r'product-specifications', ProductSpecificationViewSet)
router.register(r'product-images', ProductImageViewSet)
router.register(r'product-documents', ProductDocumentViewSet)
router.register(r'related-products', RelatedProductViewSet)
router.register(r'warehouses', WarehouseViewSet)
router.register(r'stock-levels', StockLevelViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('products/', include(router.urls)),
]
