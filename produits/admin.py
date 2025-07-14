from django.contrib import admin

# Register your models here.
from .models import Product  , Brand , Category ,ProductAttribute , ProductAttributeValues, ProductTypeAttribute


admin.site.register(Product)
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(ProductAttribute)
admin.site.register(ProductAttributeValues)
admin.site.register(ProductTypeAttribute)