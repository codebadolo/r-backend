import os
import json
from django.core.management.base import BaseCommand
from django.db import transaction

from produits.models import (
    Category, Brand, Warehouse,
    SpecCategory, SpecKey, Product, ProductVariant,
    ProductSpecification, StockLevel
)

class Command(BaseCommand):
    help = 'Importe les données produit et relatives à partir des fichiers JSON dans le répertoire courant'

    def handle(self, *args, **options):
        base_path = os.path.dirname(os.path.abspath(__file__))

        try:
            with transaction.atomic():
                self.stdout.write("Import des catégories...")
                self.load_categories(os.path.join(base_path, 'categories.json'))

                self.stdout.write("Import des marques...")
                self.load_brands(os.path.join(base_path, 'brands.json'))

                self.stdout.write("Import des entrepôts...")
                self.load_warehouses(os.path.join(base_path, 'warehouses.json'))

                self.stdout.write("Import des catégories de spécifications...")
                self.load_spec_categories(os.path.join(base_path, 'spec_categories.json'))

                self.stdout.write("Import des clés de spécifications...")
                self.load_spec_keys(os.path.join(base_path, 'spec_keys.json'))

                self.stdout.write("Import des produits...")
                self.load_products(os.path.join(base_path, 'products.json'))

                self.stdout.write("Import des variantes...")
                self.load_variants(os.path.join(base_path, 'product_variants.json'))

                self.stdout.write("Import des spécifications produits...")
                self.load_product_specifications(os.path.join(base_path, 'product_specifications.json'))

                self.stdout.write("Import des niveaux de stock...")
                self.load_stock_levels(os.path.join(base_path, 'stock_levels.json'))

                self.stdout.write(self.style.SUCCESS("Import terminé avec succès !"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Erreur pendant l'import : {e}"))

    def load_categories(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            categories = json.load(f)

        for cat in categories:
            parent = None
            parent_name = cat.get('parent_category')
            if parent_name:
                parent = Category.objects.filter(nom=parent_name).first()
            obj, created = Category.objects.update_or_create(
                nom=cat['nom'],
                defaults={
                    'description': cat.get('description'),
                    'parent_category': parent
                }
            )
            self.stdout.write(f"Catégorie importée: {obj.nom}")

    def load_brands(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            brands = json.load(f)

        for b in brands:
            obj, created = Brand.objects.update_or_create(
                nom=b['nom'],
                defaults={
                    'logo_url': b.get('logo_url'),
                    'description': b.get('description')
                }
            )
            self.stdout.write(f"Marque importée: {obj.nom}")

    def load_warehouses(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            warehouses = json.load(f)

        for w in warehouses:
            obj, created = Warehouse.objects.update_or_create(
                nom=w['nom'],
                defaults={
                    'adresse': w.get('adresse'),
                    'code_postal': w.get('code_postal'),
                    'ville': w.get('ville'),
                    'pays': w.get('pays'),
                    'type': w.get('type'),
                    'is_active': w.get('is_active', True),
                    'commentaire': w.get('commentaire', '')
                }
            )
            self.stdout.write(f"Entrepôt importé: {obj.nom}")

    def load_stock_levels(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            stocks = json.load(f)

        for stock in stocks:
            warehouse = Warehouse.objects.filter(nom=stock['warehouse']).first()
            if not warehouse:
                self.stdout.write(self.style.WARNING(f"Entrepôt non trouvé: {stock['warehouse']}"))
                continue

            product = Product.objects.filter(nom=stock['product_nom']).first()
            if not product:
                self.stdout.write(self.style.WARNING(f"Produit non trouvé pour stock: {stock['product_nom']}"))
                continue

            variant = None
            variant_nom = stock.get('variant_nom')
            if variant_nom:
                # Recherche variante avec nom + valeur concaténés ou adaptation selon votre modèle
                variant = ProductVariant.objects.filter(product=product, nom__iexact=variant_nom).first()
                if not variant:
                    self.stdout.write(self.style.WARNING(f"Variante non trouvée: {variant_nom} pour produit {product.nom}"))

            obj, created = StockLevel.objects.update_or_create(
                warehouse=warehouse,
                product=product,
                variant=variant,
                defaults={
                    'stock_total': stock.get('stock_total', 0),
                    'stock_reserve': stock.get('stock_reserve', 0),
                    'seuil_alerte': stock.get('seuil_alerte', 0)
                }
            )
            self.stdout.write(f"Stock importé: Produit {product.nom}, Entrepôt {warehouse.nom}, Stock {obj.stock_total}")

    def load_spec_categories(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            spec_categories = json.load(f)

        for sc in spec_categories:
            obj, created = SpecCategory.objects.update_or_create(
                nom=sc['nom'],
                defaults={'description': sc.get('description')}
            )
            self.stdout.write(f"Catégorie de spécification importée: {obj.nom}")

    def load_spec_keys(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            spec_keys = json.load(f)

        for sk in spec_keys:
            spec_category = SpecCategory.objects.filter(nom=sk['spec_category']).first()
            if spec_category is None:
                self.stdout.write(self.style.WARNING(f"SpecCategory {sk['spec_category']} non trouvée pour clé {sk['nom_attribut']}"))
                continue

            obj, created = SpecKey.objects.update_or_create(
                nom_attribut=sk['nom_attribut'],
                spec_category=spec_category,
                defaults={
                    'data_type': sk.get('data_type'),
                    'unit': sk.get('unit'),
                    'is_filterable': sk.get('is_filterable', False),
                    'position': sk.get('position', 0),
                    'description': sk.get('description', '')
                }
            )
            self.stdout.write(f"Clé de spécification importée: {obj.nom_attribut}")

    def load_products(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            products = json.load(f)

        for p in products:
            category = Category.objects.filter(nom=p['category']).first()
            brand = Brand.objects.filter(nom=p['brand']).first()
            if category is None or brand is None:
                self.stdout.write(self.style.WARNING(f"Catégorie ou marque non trouvée pour le produit {p['nom']}"))
                continue

            obj, created = Product.objects.update_or_create(
                nom=p['nom'],
                defaults={
                    'description': p.get('description'),
                    'prix': p.get('prix', 0),
                    'stock': p.get('stock', 0),
                    'etat': p.get('etat', 'disponible'),
                    'ean_code': p.get('ean_code'),
                    'is_active': p.get('is_active', True),
                    'category': category,
                    'brand': brand,
                }
            )
    def load_product_specifications(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            specs = json.load(f)

        for sp in specs:
            product = Product.objects.filter(nom=sp['product_nom']).first()
            if not product:
                self.stdout.write(self.style.WARNING(f"Produit non trouvé pour spécification: {sp.get('nom_attribut')} (produit {sp.get('product_nom')})"))
                continue

            spec_key = SpecKey.objects.filter(nom_attribut=sp['nom_attribut']).first()
            if not spec_key:
                self.stdout.write(self.style.WARNING(f"Clé de spécification non trouvée: {sp.get('nom_attribut')}"))
                continue

            obj, created = ProductSpecification.objects.update_or_create(
                product=product,
                spec_key=spec_key,
                defaults={'valeur': sp.get('valeur')}
            )
            self.stdout.write(f"Spécification importée: {product.nom} - {spec_key.nom_attribut}")
            
    def load_variants(self, filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            variants = json.load(f)

        for v in variants:
            product = Product.objects.filter(nom=v['product_nom']).first()
            if product is None:
                self.stdout.write(self.style.WARNING(f"Produit non trouvé pour variante: {v.get('nom')} (produit {v.get('product_nom')})"))
                continue

            obj, created = ProductVariant.objects.update_or_create(
                product=product,
                nom=v.get('nom'),
                valeur=v.get('valeur'),
                defaults={
                    'prix_supplémentaire': v.get('prix_supplémentaire', 0),
                    'stock': v.get('stock', 0),
                    'image_url': v.get('image_url', '')
                }
            )
            self.stdout.write(f"Variante importée pour {product.nom} : {obj.nom} - {obj.valeur}")
