import json
import os
from django.core.management.base import BaseCommand
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen

from produits.models import (
    Category, Brand, ProductType, Product,
    ProductAttribute, ProductAttributeOption, ProductAttributeValue,
    ProductImage, Stock
)
from django.core.files import File

class Command(BaseCommand):
    help = "Seed your catalog from products_full.json (same directory as this script!)"

    def handle(self, *args, **kwargs):
        base = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base, 'products_full.json')
        if not os.path.isfile(json_path):
            self.stderr.write(self.style.ERROR(f"products_full.json not found in {base}"))
            return
        
        with open(json_path, encoding="utf-8") as f:
            products = json.load(f)

        for idx, data in enumerate(products, start=1):
            # Get or create related objects
            category, _ = Category.objects.get_or_create(name=data['category'])
            brand, _ = Brand.objects.get_or_create(name=data['brand'])
            ptype, _ = ProductType.objects.get_or_create(name=data['product_type'])

            # Create or get product
            product, created = Product.objects.get_or_create(
                name=data['name'],
                category=category,
                brand=brand,
                product_type=ptype,
                defaults={
                    "description": data.get("description", ""),
                    "price": data["price"],
                    "is_active": data.get("is_active", True),
                }
            )

            # Attributes: create attribute, option, and link as ProductAttributeValue
            for attr in data.get("attributes", []):
                attribute, _ = ProductAttribute.objects.get_or_create(
                    name=attr["attribute_name"], product_type=ptype
                )
                option, _ = ProductAttributeOption.objects.get_or_create(
                    attribute=attribute,
                    value=attr["value"]
                )
                ProductAttributeValue.objects.get_or_create(
                    product=product,
                    option=option
                )

            # Images
            for img in data.get("images", []):
                if not ProductImage.objects.filter(product=product, alt_text=img.get("alt_text", "")).exists():
                    img_url = img["url"]
                    alt = img.get("alt_text", "")
                    try:
                        img_temp = NamedTemporaryFile(delete=True)
                        with urlopen(img_url) as u:
                            img_temp.write(u.read())
                            img_temp.flush()
                        file_basename = os.path.basename(img_url).split("?")[0]
                        img_obj = ProductImage(product=product, alt_text=alt, is_feature=False)
                        img_obj.image.save(file_basename, File(img_temp), save=True)
                    except Exception as exc:
                        self.stderr.write(self.style.WARNING(
                            f"Could not fetch image for {product.name}: {img_url} ({exc})"
                        ))

            # Stock
            s = data.get("stock")
            if s:
                Stock.objects.update_or_create(
                    product=product,
                    defaults={
                        "units": s.get("units", 0),
                        "units_sold": s.get("units_sold", 0)
                    }
                )

            self.stdout.write(self.style.SUCCESS(f"{idx}. {product.name} imported ✓"))

        self.stdout.write(self.style.SUCCESS(f"{len(products)} products imported."))
