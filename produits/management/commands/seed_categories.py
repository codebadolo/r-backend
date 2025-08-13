from django.core.management.base import BaseCommand
from produits.models import Category

CATEGORIES_DATA = [
    {"nom": "Télécommunications & navigation", "description": None, "parent_category": None},
    {"nom": "Équipements de conférence", "description": None, "parent_category": "Télécommunications & navigation"},
    {"nom": "Équipements de communication radio", "description": None, "parent_category": "Télécommunications & navigation"},
    {"nom": "Équipement téléphonique", "description": None, "parent_category": "Télécommunications & navigation"},
    {"nom": "Équipement de gestion des appels", "description": None, "parent_category": "Télécommunications & navigation"},
    {"nom": "Consommables intelligents", "description": None, "parent_category": None},
    {"nom": "Dispositifs de communication mobile", "description": None, "parent_category": None},
    {"nom": "Equipements de navigation", "description": None, "parent_category": "Télécommunications & navigation"},
    {"nom": "Accessoires d'équipements de télécommunications", "description": None, "parent_category": "Télécommunications & navigation"},
    {"nom": "Informatique & électronique", "description": None, "parent_category": None},
    {"nom": "Réseaux", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Composants", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Ordinateurs", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Logiciels", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Garanties et supports", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Imprimantes et scanners", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Câbles pour ordinateurs et périphériques", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Stockages de données", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Écrans et accessoires", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Piles et alimentations électriques", "description": None, "parent_category": None},
    {"nom": "Entrées de données et commandes", "description": None, "parent_category": "Informatique & électronique"},
    {"nom": "Automatisation de la maison et sécurité", "description": None, "parent_category": None},
    {"nom": "Systèmes de surveillance", "description": None, "parent_category": "Automatisation de la maison et sécurité"},
    {"nom": "Accès et contrôles", "description": None, "parent_category": "Automatisation de la maison et sécurité"},
    {"nom": "Appareils intelligents pour la maison", "description": None, "parent_category": "Automatisation de la maison et sécurité"},
    {"nom": "Capteurs et alarmes domestiques", "description": None, "parent_category": "Automatisation de la maison et sécurité"},
    {"nom": "Dispositifs de sécurité", "description": None, "parent_category": "Automatisation de la maison et sécurité"},
    {"nom": "Produits de sécurité des installations", "description": None, "parent_category": "Automatisation de la maison et sécurité"},
    {"nom": "Protections contre le feu", "description": None, "parent_category": "Automatisation de la maison et sécurité"},
    {"nom": "Protection contre les inondations", "description": None, "parent_category": "Automatisation de la maison et sécurité"},
    {"nom": "Équipements électriques et fournitures", "description": None, "parent_category": None},
    {"nom": "Dispositifs et accessoires de câblage", "description": None, "parent_category": "Équipements électriques et fournitures"},
    {"nom": "Protections pour circuit", "description": None, "parent_category": "Équipements électriques et fournitures"},
    {"nom": "Matériau et fournitures électriques", "description": None, "parent_category": "Équipements électriques et fournitures"},
    {"nom": "Conditionnement de puissance", "description": None, "parent_category": "Équipements électriques et fournitures"},
    {"nom": "Conduits de chemin de cables", "description": None, "parent_category": "Équipements électriques et fournitures"},
    {"nom": "Générateurs électriques", "description": None, "parent_category": "Équipements électriques et fournitures"},
    {"nom": "Dispositifs de commande électrique", "description": None, "parent_category": "Équipements électriques et fournitures"},
    {"nom": "Boites éléctriques et accessoires", "description": None, "parent_category": "Équipements électriques et fournitures"},
    {"nom": "Photovoltaïque", "description": None, "parent_category": None},
    {"nom": "Kits photovoltaïques", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Panneaux photovoltaïques", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Onduleurs", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Systèmes de stockage d'énergie", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Optimisateurs de puissance", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Chargement de voitures", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Pompes à chaleur", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Climatiseurs", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Stations d'alimentation portables", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Panneaux solaires", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Turbines éoliennes", "description": None, "parent_category": "Photovoltaïque"},
    {"nom": "Boîtiers de raccordement", "description": None, "parent_category": None},
    {"nom": "Câbles", "description": None, "parent_category": None},
    {"nom": "Éléments électriques", "description": None, "parent_category": None},
    {"nom": "Compteurs d'énergie", "description": None, "parent_category": None},
    {"nom": "Structures de montage", "description": None, "parent_category": None},
    {"nom": "Suivi d'installation", "description": None, "parent_category": None},
    {"nom": "Accessoires pour onduleurs", "description": None, "parent_category": None},
    {"nom": "Micro-onduleurs", "description": None, "parent_category": None},
    {"nom": "Technologie de chauffage", "description": None, "parent_category": None},
    {"nom": "Outils", "description": None, "parent_category": None},
    {"nom": "Équipements audiovisuels", "description": None, "parent_category": None},
    {"nom": "Fournitures de présentation", "description": None, "parent_category": None},
    {"nom": "Casques audio et portables", "description": None, "parent_category": "Équipements audiovisuels"},
    {"nom": "Pièces et accessoires d'équipements audiovisuels", "description": None, "parent_category": "Équipements audiovisuels"},
    {"nom": "Projecteurs", "description": None, "parent_category": "Équipements audiovisuels"},
    {"nom": "Télévisions", "description": None, "parent_category": "Équipements audiovisuels"},
    {"nom": "Distributions et traitements du signal", "description": None, "parent_category": "Équipements audiovisuels"},
    {"nom": "Systèmes audios domestiques", "description": None, "parent_category": "Équipements audiovisuels"},
    {"nom": "Équipement photo et vidéo", "description": None, "parent_category": None},
    {"nom": "Appareils photo et caméscopes", "description": None, "parent_category": "Équipement photo et vidéo"},
    {"nom": "Accessoires pour caméras", "description": None, "parent_category": "Équipement photo et vidéo"},
    {"nom": "Signalisations", "description": None, "parent_category": None},
    {"nom": "Écran d'affichage dynamique", "description": None, "parent_category": "Signalisations"},
    {"nom": "Accessoires d’écran de mur vidéo", "description": None, "parent_category": "Signalisations"},
    {"nom": "Murs d'écrans vidéos", "description": None, "parent_category": "Signalisations"},
    {"nom": "Montages des affichages de messages", "description": None, "parent_category": "Signalisations"},
    {"nom": "Accessoires d'affichage de messages", "description": None, "parent_category": "Signalisations"},
]

class Command(BaseCommand):
    help = 'Insère une liste de catégories avec gestion des catégories parentes'

    def handle(self, *args, **options):
        # Première passe : création des catégories racines (parent_category=None)
        parent_categories = {}
        for cat_data in CATEGORIES_DATA:
            if cat_data['parent_category'] is None:
                category, created = Category.objects.get_or_create(
                    nom=cat_data['nom'],
                    defaults={'description': cat_data['description']}
                )
                parent_categories[cat_data['nom']] = category
                if created:
                    self.stdout.write(self.style.SUCCESS(f"Catégorie racine créée: {category.nom}"))
                else:
                    self.stdout.write(f"Catégorie racine existante: {category.nom}")
        
        # Deuxième passe : création des sous-catégories avec liaison au parent
        for cat_data in CATEGORIES_DATA:
            parent_name = cat_data['parent_category']
            if parent_name is not None:
                parent_cat = parent_categories.get(parent_name) or Category.objects.filter(nom=parent_name).first()
                if not parent_cat:
                    self.stdout.write(self.style.ERROR(f"Catégorie parent introuvable: {parent_name} pour {cat_data['nom']}"))
                    continue
                category, created = Category.objects.get_or_create(
                    nom=cat_data['nom'],
                    defaults={
                        'description': cat_data['description'],
                        'parent_category': parent_cat
                    }
                )
                # Si la catégorie existe déjà mais pas liée au parent, on met à jour
                if not created and category.parent_category != parent_cat:
                    category.parent_category = parent_cat
                    category.description = cat_data['description']
                    category.save()
                    self.stdout.write(self.style.SUCCESS(f"Catégorie mise à jour avec parent: {category.nom}"))
                else:
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"Sous-catégorie créée: {category.nom} (parent: {parent_cat.nom})"))
                    else:
                        self.stdout.write(f"Sous-catégorie existante: {category.nom} (parent: {parent_cat.nom})")

        self.stdout.write(self.style.SUCCESS("Insertion / mise à jour des catégories terminée."))
