import os
import json
from django.core.management.base import BaseCommand
from django.utils.text import slugify
from produits.models import (
    Brand, Category, ProductType, Product, ProductAttribute, ProductAttributeValue,
    ProductTypeAttribute, ProductInventory, ProductAttributeValues,
    SectionSpecification, CleSpecification, ProduitSpecification, Media
)

class Command(BaseCommand):
    help = "Charge des produits complets (toutes étapes) depuis un fichier JSON"

    def add_arguments(self, parser):
        parser.add_argument(
            '--file',
            type=str,
            default=None,
            help='Chemin du fichier JSON à charger'
        )

    def handle(self, *args, **options):
        # 1. Déterminer le chemin du fichier JSON
        if options['file']:
            file_path = options['file']
        else:
            file_path = os.path.join(os.path.dirname(__file__), 'products_full.json')

        self.stdout.write(self.style.NOTICE(f"Chargement depuis {file_path}"))

        # 2. Charger les données JSON
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"Fichier introuvable: {file_path}"))
            return

        with open(file_path, 'r', encoding='utf-8') as f:
            products = json.load(f)

        for idx, pdata in enumerate(products, 1):
            # 1. Infos générales
            brand, _ = Brand.objects.get_or_create(name=pdata['brand'])
            parent_cat = None
            if pdata.get('category_parent'):
                parent_cat, _ = Category.objects.get_or_create(name=pdata['category_parent'])
            category, _ = Category.objects.get_or_create(name=pdata['category'], parent=parent_cat)
            ptype, _ = ProductType.objects.get_or_create(name=pdata['product_type'])
            product, _ = Product.objects.get_or_create(
                name=pdata['name'],
                defaults={
                    'web_id': slugify(pdata['name'])[:100],
                    'description': pdata.get('description', ''),
                    'category': category,
                    'brand': brand,
                    'product_type': ptype,
                }
            )

            # 2. Attributs et liaison au type
            for attr in pdata.get('attributes', []):
                attr_obj, _ = ProductAttribute.objects.get_or_create(name=attr['name'])
                ProductTypeAttribute.objects.get_or_create(product_type=ptype, product_attribute=attr_obj)
                ProductAttributeValue.objects.get_or_create(product_attribute=attr_obj, value=attr['value'])

            # 3. Variantes (ProductInventory + valeurs)
            for variant in pdata.get('variants', []):
                inv, _ = ProductInventory.objects.get_or_create(
                    sku=variant['sku'],
                    defaults={
                        'product_type': ptype,
                        'product': product,
                        'brand': brand,
                        'retail_price': variant['retail_price'],
                        'store_price': variant['store_price'],
                        'is_default': variant.get('is_default', False),
                    }
                )
                # Lier valeurs d'attribut à la variante
                for val in variant.get('values', []):
                    attr_obj = ProductAttribute.objects.get(name=val['name'])
                    val_obj, _ = ProductAttributeValue.objects.get_or_create(product_attribute=attr_obj, value=val['value'])
                    ProductAttributeValues.objects.get_or_create(product_attribute_value=val_obj, product_inventory=inv)

            # 4. Spécifications techniques
            for spec in pdata.get('specifications', []):
                section, _ = SectionSpecification.objects.get_or_create(name=spec['section'])
                key, _ = CleSpecification.objects.get_or_create(name=spec['key'], section=section)
                ProduitSpecification.objects.get_or_create(product=product, cle_specification=key, value=spec['value'])

            # 5. Images (Media)
            for img in pdata.get('images', []):
                inv = ProductInventory.objects.filter(product=product).first()
                Media.objects.get_or_create(
                    product_inventory=inv,
                    img_url=img['img_url'],
                    defaults={
                        'alt_text': img.get('alt_text', ''),
                        'is_feature': img.get('is_feature', False)
                    }
                )
            self.stdout.write(self.style.SUCCESS(f"Produit '{product.name}' chargé avec variantes, specs et images."))

        self.stdout.write(self.style.SUCCESS(f"{len(products)} produits complets importés avec succès !"))
