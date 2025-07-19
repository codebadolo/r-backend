import json
import os
from django.core.management.base import BaseCommand
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen

from produits.models import (
    Category, Brand, ProductType, Product,
    ProductAttribute, ProductAttributeOption, ProductAttributeValue,
    ProductImage, Stock, Warehouse
)
from django.core.files import File


class Command(BaseCommand):
    help = "Seed your catalog from products_full.json with warehouses"

    def handle(self, *args, **kwargs):
        base = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base, 'products_full.json')
        if not os.path.isfile(json_path):
            self.stderr.write(self.style.ERROR(f"products_full.json not found in {base}"))
            return

        # 1. Create warehouses upfront
        warehouses_data = [
            {"name": "Ouagadougou Central Warehouse", "location": "Zone industrielle, Ouagadougou"},
            {"name": "Bobo-Dioulasso Storage", "location": "Quartier Dioulassoba, Bobo-Dioulasso"},
            {"name": "Koudougou Depot", "location": "Périphérie Sud, Koudougou"},
            {"name": "Banfora Regional Warehouse", "location": "PK7, Banfora"},
            {"name": "Ouahigouya Logistics Center", "location": "Zone commerciale, Ouahigouya"},
        ]
        warehouse_map = {}
        for wh in warehouses_data:
            warehouse_obj, created = Warehouse.objects.get_or_create(
                name=wh["name"],
                defaults={"location": wh["location"]}
            )
            warehouse_map[wh["name"]] = warehouse_obj

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

            # Images: Because of 403 Forbidden issues, we skip downloading and just log warning.
            for img in data.get("images", []):
                if not ProductImage.objects.filter(product=product, alt_text=img.get("alt_text", "")).exists():
                    img_url = img["url"]
                    alt = img.get("alt_text", "")
                    self.stderr.write(self.style.WARNING(
                        f"Skipping image download due to possible access denial: {img_url} (Product: {product.name})"
                    ))
                    # TODO: optionally, store the URL in a separate field if your model supports it

            # Stock & warehouse assignment
            stock_data = data.get("stock")
            if stock_data:
                warehouse_id = stock_data.get("warehouse_id")
                warehouse_name = stock_data.get("warehouse_name")  # alternatively, accept by name

                warehouse = None
                if warehouse_id is not None:
                    try:
                        warehouse = Warehouse.objects.get(id=warehouse_id)
                    except Warehouse.DoesNotExist:
                        self.stderr.write(self.style.ERROR(
                            f"Warehouse with id {warehouse_id} not found for product '{product.name}'"
                        ))
                elif warehouse_name:
                    warehouse = warehouse_map.get(warehouse_name)
                    if warehouse is None:
                        self.stderr.write(self.style.ERROR(
                            f"Warehouse with name '{warehouse_name}' not found for product '{product.name}'"
                        ))
                else:
                    # fallback to a default warehouse (e.g. Ouagadougou Central Warehouse)
                    warehouse = warehouse_map.get("Ouagadougou Central Warehouse")

                if warehouse:
                    Stock.objects.update_or_create(
                        product=product,
                        warehouse=warehouse,
                        defaults={
                            "units": stock_data.get("units", 0),
                            "units_sold": stock_data.get("units_sold", 0),
                        }
                    )
                else:
                    self.stderr.write(self.style.ERROR(
                        f"No valid warehouse for product '{product.name}', skipping stock creation"
                    ))

            self.stdout.write(self.style.SUCCESS(f"{idx}. {product.name} imported ✓"))

        self.stdout.write(self.style.SUCCESS(f"{len(products)} products imported."))
