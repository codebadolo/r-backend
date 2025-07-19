from produits.models import (
    Category, Brand, ProductType, Product,
    ProductAttribute, ProductAttributeOption,
    ProductAttributeValue, ProductImage,
    Warehouse, Stock
)


ProductAttributeValue.objects.all().delete()
ProductAttributeOption.objects.all().delete()
ProductAttribute.objects.all().delete()

ProductImage.objects.all().delete()
Stock.objects.all().delete()

Product.objects.all().delete()
Category.objects.all().delete()
Brand.objects.all().delete()
ProductType.objects.all().delete()
Warehouse.objects.all().delete()
