import json
import os
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from django.utils.timezone import now
from produits.models import (
    Category, Brand, Product, ProductVariant,
    SpecCategory, SpecKey, ProductSpecification,
    ProductImage, ProductDocument, RelatedProduct,
    Warehouse, StockLevel, StockMovement
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUCT_JSON_PATH = os.path.join(BASE_DIR, 'products.json')
IMAGES_FOLDER = os.path.join(settings.MEDIA_ROOT, 'product_images')


class Command(BaseCommand):
    help = 'Importer plusieurs produits depuis un fichier JSON (liste) avec gestion stock/warehouses'

    def handle(self, *args, **options):
        if not os.path.exists(PRODUCT_JSON_PATH):
            self.stderr.write(f"Fichier JSON introuvable : {PRODUCT_JSON_PATH}")
            return

        with open(PRODUCT_JSON_PATH, 'r', encoding='utf-8') as f:
            products_list = json.load(f)

        for data in products_list:
            self.stdout.write(f'--- Traitement produit: {data.get("product", {}).get("nom")} ---')

            # --- Gestion catégorie ---
            category_data = data.get('category')
            parent_category_obj = None
            if category_data.get('parent_category'):
                parent_category_obj, _ = Category.objects.get_or_create(nom=category_data['parent_category'])

            category_obj, _ = Category.objects.get_or_create(
                nom=category_data['nom'],
                defaults={
                    'description': category_data.get('description'),
                    'parent_category': parent_category_obj
                }
            )

            # --- Gestion marque ---
            brand_data = data.get('brand')
            brand_obj, _ = Brand.objects.get_or_create(
                nom=brand_data['nom'],
                defaults={'description': brand_data.get('description')}
            )

            # --- Gestion produit ---
            prod_data = data.get('product')
            product_obj, created = Product.objects.get_or_create(
                nom=prod_data['nom'],
                defaults={
                    'category': category_obj,
                    'brand': brand_obj,
                    'description': prod_data.get('description'),
                    'prix': prod_data.get('prix'),
                    'stock': prod_data.get('stock'),
                    'etat': prod_data.get('etat', 'disponible'),
                    'ean_code': prod_data.get('ean_code'),
                    'is_active': prod_data.get('is_active', True),
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Produit créé: {product_obj.nom}"))
            else:
                self.stdout.write(f"Produit existant: {product_obj.nom}")

            # --- Gestion variantes ---
            variants_data = data.get('variants', [])
            for variant_group in variants_data:
                variant_name = variant_group['nom']
                for val in variant_group['valeurs']:
                    variant_obj, v_created = ProductVariant.objects.get_or_create(
                        product=product_obj,
                        nom=variant_name,
                        valeur=val['valeur'],
                        defaults={
                            'prix_supplémentaire': val.get('prix_supplémentaire', 0),
                            'stock': val.get('stock', 0),
                        }
                    )
                    # Gestion image variante
                    if 'image' in val and val['image']:
                        image_path = os.path.join(IMAGES_FOLDER, val['image'])
                        if os.path.exists(image_path):
                            with open(image_path, 'rb') as img_file:
                                django_file = File(img_file)
                                variant_obj.image.save(val['image'], django_file, save=True)
                            self.stdout.write(self.style.SUCCESS(f"Image variante ajoutée: {val['image']}"))
                        else:
                            self.stdout.write(self.style.WARNING(f"Image variante non trouvée : {image_path}"))
                    if v_created:
                        self.stdout.write(self.style.SUCCESS(f"Variante créée: {variant_obj}"))
                    else:
                        self.stdout.write(f"Variante existante: {variant_obj}")

            # --- Gestion spécifications ---
            specs_data = data.get('specifications', [])
            for spec_cat_data in specs_data:
                spec_category_obj, cat_created = SpecCategory.objects.get_or_create(
                    nom=spec_cat_data['spec_category']
                )
                if cat_created:
                    self.stdout.write(self.style.SUCCESS(f"Catégorie spécification créée: {spec_category_obj.nom}"))

                for attr in spec_cat_data['attributes']:
                    spec_key_obj, key_created = SpecKey.objects.get_or_create(
                        spec_category=spec_category_obj,
                        nom_attribut=attr['nom_attribut'],
                        defaults={
                            'data_type': attr['data_type'],
                            'unit': attr.get('unit'),
                            'is_filterable': True,
                            'position': 0,
                            'description': '',
                        }
                    )
                    if key_created:
                        self.stdout.write(self.style.SUCCESS(f"Clé spécification créée: {spec_key_obj.nom_attribut}"))

                    ps_obj, ps_created = ProductSpecification.objects.get_or_create(
                        product=product_obj,
                        spec_key=spec_key_obj,
                        defaults={'valeur': attr['valeur']}
                    )
                    if ps_created:
                        self.stdout.write(self.style.SUCCESS(f"Spécification ajoutée: {spec_key_obj.nom_attribut} = {attr['valeur']}"))

            # --- Gestion images produit ---
            images_data = data.get('images', [])
            for img in images_data:
                image_path = os.path.join(IMAGES_FOLDER, img['image'])
                product_image_obj, img_created = ProductImage.objects.get_or_create(
                    product=product_obj,
                    alt_text=img.get('alt_text', '')
                )
                if img_created:
                    if os.path.exists(image_path):
                        with open(image_path, 'rb') as img_file:
                            django_file = File(img_file)
                            product_image_obj.image.save(os.path.basename(image_path), django_file, save=True)
                        self.stdout.write(self.style.SUCCESS(f"Image produit ajoutée: {img['image']}"))
                    else:
                        self.stdout.write(self.style.WARNING(f"Image produit non trouvée: {image_path}"))
                else:
                    self.stdout.write(f"Image produit existante: {img['image']}")

            # --- Gestion documents ---
            documents_data = data.get('documents', [])
            for doc in documents_data:
                doc_obj, doc_created = ProductDocument.objects.get_or_create(
                    product=product_obj,
                    url_document=doc['url_document'],
                    defaults={'type_document': doc.get('type_document')}
                )
                if doc_created:
                    self.stdout.write(self.style.SUCCESS(f"Document ajouté: {doc['url_document']}"))
                else:
                    self.stdout.write(f"Document existant: {doc['url_document']}")

            # --- Gestion produits liés ---
            related_products_data = data.get('related_products', [])
            for related in related_products_data:
                try:
                    related_prod = Product.objects.get(nom=related['related_product_nom'])
                except Product.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f"Produit lié introuvable: {related['related_product_nom']}"))
                    continue

                rel_obj, rel_created = RelatedProduct.objects.get_or_create(
                    product=product_obj,
                    related_product=related_prod,
                    defaults={'relation_type': related.get('relation_type')}
                )
                if rel_created:
                    self.stdout.write(self.style.SUCCESS(f"Produit lié ajouté: {related_prod.nom}"))
                else:
                    self.stdout.write(f"Produit lié existant: {related_prod.nom}")

            # --- Gestion warehouses (entrepôts) et stocks ---
            warehouses_data = data.get('warehouses', [])
            warehouse_objs = {}

            for wh_data in warehouses_data:
                warehouse_obj, wh_created = Warehouse.objects.get_or_create(
                    nom=wh_data['nom'],
                    defaults={
                        'adresse': wh_data.get('adresse', ''),
                        'code_postal': wh_data.get('code_postal', ''),
                        'ville': wh_data.get('ville', ''),
                        'pays': wh_data.get('pays', ''),
                        'type': wh_data.get('type', 'physique'),
                        'is_active': wh_data.get('is_active', True),
                        'commentaire': wh_data.get('commentaire', '')
                    }
                )
                # Mise à jour info si nécessaire
                if not wh_created:
                    updated = False
                    for field in ['adresse','code_postal','ville','pays','type','is_active','commentaire']:
                        val = wh_data.get(field)
                        if val is not None and getattr(warehouse_obj, field) != val:
                            setattr(warehouse_obj, field, val)
                            updated = True
                    if updated:
                        warehouse_obj.save()
                warehouse_objs[warehouse_obj.nom] = warehouse_obj

                # Stock produit global en entrepôt
                stock_total = wh_data.get('stock_total', 0)
                stock_reserve = wh_data.get('stock_reserve', 0)
                seuil_alerte = wh_data.get('seuil_alerte', 0)

                stock_level_obj, sl_created = StockLevel.objects.get_or_create(
                    warehouse=warehouse_obj,
                    product=product_obj,
                    variant=None,
                    defaults={
                        'stock_total': stock_total,
                        'stock_reserve': stock_reserve,
                        'seuil_alerte': seuil_alerte
                    }
                )
                if not sl_created:
                    stock_level_obj.stock_total = stock_total
                    stock_level_obj.stock_reserve = stock_reserve
                    stock_level_obj.seuil_alerte = seuil_alerte
                    stock_level_obj.save()

                StockMovement.objects.create(
                    warehouse=warehouse_obj,
                    product=product_obj,
                    variant=None,
                    mouvement_type='réception',
                    quantite=stock_total,
                    commentaire=f'Stock initial produit global dans l\'entrepôt {warehouse_obj.nom}',
                    date_mouvement=now(),
                    user=None
                )

            # --- Stocks par variante et entrepôt ---
            variant_warehouses_stock = data.get('variant_warehouses_stock', [])
            for variant_stock_info in variant_warehouses_stock:
                v_nom = variant_stock_info.get('variant_nom')
                v_valeur = variant_stock_info.get('variant_valeur')
                warehouses_stock = variant_stock_info.get('warehouses', [])

                variant_obj = ProductVariant.objects.filter(
                    product=product_obj,
                    nom=v_nom,
                    valeur=v_valeur
                ).first()

                if not variant_obj:
                    self.stdout.write(self.style.WARNING(f"Variante introuvable pour stock entrepôt: {v_nom} = {v_valeur}"))
                    continue

                for wh_stock in warehouses_stock:
                    wh_name = wh_stock.get('nom')
                    wh_obj = warehouse_objs.get(wh_name)

                    if not wh_obj:
                        self.stdout.write(self.style.WARNING(f"Entrepôt introuvable pour stock variante : {wh_name}"))
                        continue

                    stock_total = wh_stock.get('stock_total', 0)
                    stock_reserve = wh_stock.get('stock_reserve', 0)
                    seuil_alerte = wh_stock.get('seuil_alerte', 0)

                    stock_level_obj, sl_created = StockLevel.objects.get_or_create(
                        warehouse=wh_obj,
                        product=product_obj,
                        variant=variant_obj,
                        defaults={
                            'stock_total': stock_total,
                            'stock_reserve': stock_reserve,
                            'seuil_alerte': seuil_alerte
                        }
                    )
                    if not sl_created:
                        stock_level_obj.stock_total = stock_total
                        stock_level_obj.stock_reserve = stock_reserve
                        stock_level_obj.seuil_alerte = seuil_alerte
                        stock_level_obj.save()

                    StockMovement.objects.create(
                        warehouse=wh_obj,
                        product=product_obj,
                        variant=variant_obj,
                        mouvement_type='réception',
                        quantite=stock_total,
                        commentaire=f'Stock initial variante {variant_obj.nom}={variant_obj.valeur} dans entrepôt {wh_obj.nom}',
                        date_mouvement=now(),
                        user=None
                    )

            self.stdout.write(self.style.SUCCESS(f"Traitement terminé pour le produit: {product_obj.nom}\n"))
