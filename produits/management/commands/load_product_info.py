import json
import os
from django.core.management.base import BaseCommand
from produits.models import (
    Category, Brand, ProductType,
    ProductAttribute, ProductAttributeOption,
    Warehouse
)


class Command(BaseCommand):
    help = "Load categories, brands, product types, attributes & options, and warehouses from product_info.json"

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(base_dir, 'product_info.json')
        if not os.path.isfile(json_path):
            self.stderr.write(self.style.ERROR(f"product_info.json not found in {base_dir}"))
            return

        with open(json_path, encoding='utf-8') as f:
            data = json.load(f)

        # --- Categories (handle parent-child relationships) ---
        self.stdout.write("Importing categories...")
        # We will first create all categories without parents, then iterate to create those with parents
        name_to_category = {}
        categories_created = 0

        # First pass: parent=None categories
        for cat_data in data.get("categories", []):
            if cat_data.get("parent") is None:
                cat, created = Category.objects.get_or_create(name=cat_data["name"], parent=None)
                name_to_category[cat.name] = cat
                if created:
                    categories_created += 1

        # Second pass: categories with parents
        for cat_data in data.get("categories", []):
            parent_name = cat_data.get("parent")
            if parent_name:
                parent_cat = name_to_category.get(parent_name)
                if not parent_cat:
                    # If parent not created yet, create it as parent=None
                    parent_cat, _ = Category.objects.get_or_create(name=parent_name, parent=None)
                    name_to_category[parent_name] = parent_cat
                cat, created = Category.objects.get_or_create(name=cat_data["name"], parent=parent_cat)
                name_to_category[cat.name] = cat
                if created:
                    categories_created += 1

        self.stdout.write(self.style.SUCCESS(f"{categories_created} categories imported/updated."))

        # --- Brands ---
        self.stdout.write("Importing brands...")
        brands_created = 0
        for brand_name in data.get("brands", []):
            _, created = Brand.objects.get_or_create(name=brand_name)
            if created:
                brands_created += 1
        self.stdout.write(self.style.SUCCESS(f"{brands_created} brands imported/updated."))

        # --- Product Types ---
        self.stdout.write("Importing product types...")
        product_types_created = 0
        product_types_map = {}
        for pt_name in data.get("product_types", []):
            pt, created = ProductType.objects.get_or_create(name=pt_name)
            product_types_map[pt_name] = pt
            if created:
                product_types_created += 1
        self.stdout.write(self.style.SUCCESS(f"{product_types_created} product types imported/updated."))

        # --- Product Attributes and Options ---
        self.stdout.write("Importing product attributes and options...")
        attributes_created = 0
        options_created = 0
        for attr_data in data.get("product_attributes", []):
            pt_name = attr_data["product_type"]
            pt = product_types_map.get(pt_name)
            if not pt:
                # Create product type if missing
                pt, _ = ProductType.objects.get_or_create(name=pt_name)
                product_types_map[pt_name] = pt

            attribute, created_attr = ProductAttribute.objects.get_or_create(
                name=attr_data["name"],
                product_type=pt
            )
            if created_attr:
                attributes_created += 1

            for opt_val in attr_data.get("options", []):
                _, created_opt = ProductAttributeOption.objects.get_or_create(
                    attribute=attribute,
                    value=opt_val
                )
                if created_opt:
                    options_created += 1

        self.stdout.write(self.style.SUCCESS(
            f"{attributes_created} product attributes and {options_created} options imported/updated."
        ))

        # --- Warehouses ---
        self.stdout.write("Importing warehouses...")
        warehouses_created = 0
        for wh_data in data.get("warehouses", []):
            _, created = Warehouse.objects.get_or_create(
                name=wh_data["name"],
                defaults={"location": wh_data.get("location", "")}
            )
            if created:
                warehouses_created += 1
        self.stdout.write(self.style.SUCCESS(f"{warehouses_created} warehouses imported/updated."))

        self.stdout.write(self.style.SUCCESS("All product information loaded successfully."))
