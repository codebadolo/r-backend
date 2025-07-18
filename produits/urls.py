from django.urls import path
from . import views

urlpatterns = [
    # Category
    path('categories/', views.CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', views.CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),

    # Brand
    path('brands/', views.BrandListCreateAPIView.as_view(), name='brand-list-create'),
    path('brands/<int:pk>/', views.BrandRetrieveUpdateDestroyAPIView.as_view(), name='brand-detail'),

    # Product Type
    path('types/', views.ProductTypeListCreateAPIView.as_view(), name='type-list-create'),
    path('types/<int:pk>/', views.ProductTypeRetrieveUpdateDestroyAPIView.as_view(), name='type-detail'),

    # Product Attribute
    path('attributes/', views.ProductAttributeListCreateAPIView.as_view(), name='product-attribute-list-create'),
    path('attributes/<int:pk>/', views.ProductAttributeRetrieveUpdateDestroyAPIView.as_view(), name='product-attribute-detail'),

    # Product Attribute Value
    path('attribute-values/', views.ProductAttributeValueListCreateAPIView.as_view(), name='product-attribute-value-list-create'),
    path('attribute-values/<int:pk>/', views.ProductAttributeValueRetrieveUpdateDestroyAPIView.as_view(), name='product-attribute-value-detail'),

    path('attribute-options/', views.ProductAttributeOptionListCreateAPIView.as_view(), name='product-attribute-option-list-create'),
    path('attribute-options/<int:pk>/', views.ProductAttributeOptionRetrieveUpdateDestroyAPIView.as_view(), name='product-attribute-option-detail'),
    # Product Image
    path('images/', views.ProductImageListCreateAPIView.as_view(), name='product-image-list-create'),
    path('images/<int:pk>/', views.ProductImageRetrieveUpdateDestroyAPIView.as_view(), name='product-image-detail'),

    # Warehouse
    path('warehouses/', views.WarehouseListCreateAPIView.as_view(), name='warehouse-list-create'),
    path('warehouses/<int:pk>/', views.WarehouseRetrieveUpdateDestroyAPIView.as_view(), name='warehouse-detail'),

    # Stock
    path('stocks/', views.StockListCreateAPIView.as_view(), name='stock-list-create'),
    path('stocks/<int:pk>/', views.StockRetrieveUpdateDestroyAPIView.as_view(), name='stock-detail'),

    # Product
    path('products/', views.ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
]
