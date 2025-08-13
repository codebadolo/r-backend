from django.core.management.base import BaseCommand
from produits.models import Brand

BRANDS_DATA = [
    {"nom": "Apple", "logo_url": None, "description": "Marque leader en électronique grand public et ordinateurs"},
    {"nom": "Dell", "logo_url": None, "description": "Fabricant d'ordinateurs et solutions informatiques"},
    {"nom": "HP (Hewlett-Packard)", "logo_url": None, "description": "Entreprise spécialisée en matériel informatique et imprimantes"},
    {"nom": "Lenovo", "logo_url": None, "description": "Fabricant d'ordinateurs et équipement électronique"},
    {"nom": "Asus", "logo_url": None, "description": "Fabricant d'ordinateurs portables, cartes mères et composants"},
    {"nom": "Acer", "logo_url": None, "description": "Concepteur d'ordinateurs portables et accessoires"},
    {"nom": "Microsoft", "logo_url": None, "description": "Éditeur de logiciels et fabricant de matériel"},
    {"nom": "Intel", "logo_url": None, "description": "Leader mondial des processeurs et semi-conducteurs"},
    {"nom": "Nvidia", "logo_url": None, "description": "Spécialiste des processeurs graphiques et intelligence artificielle"},
    {"nom": "Seagate", "logo_url": None, "description": "Fabricant de disques durs et solutions stockage"},
    {"nom": "Western Digital", "logo_url": None, "description": "Fabricant de solutions de stockage"},
    {"nom": "Logitech", "logo_url": None, "description": "Accessoires informatiques et périphériques"},
    {"nom": "Razer", "logo_url": None, "description": "Équipement et accessoires gamers"},
    {"nom": "Corsair", "logo_url": None, "description": "Composants et périphériques PC"},
    {"nom": "Kingston", "logo_url": None, "description": "Mémoire et solutions stockage"},
    {"nom": "Crucial", "logo_url": None, "description": "Fabricant mémoire RAM et SSD"},
    {"nom": "MSI", "logo_url": None, "description": "Composants et ordinateurs gaming"},
    {"nom": "Fujitsu", "logo_url": None, "description": "Solutions IT et serveurs"},
    {"nom": "Samsung", "logo_url": None, "description": "Électronique grand public, mémoire et stockage"},
    {"nom": "Cisco", "logo_url": None, "description": "Equipements réseaux et télécommunications"},
    {"nom": "IBM", "logo_url": None, "description": "Technologie et services informatiques"},
    {"nom": "Netgear", "logo_url": None, "description": "Equipements réseaux domestiques et pro"},
    {"nom": "TP-Link", "logo_url": None, "description": "Equipements réseaux et Wi-Fi"},
    {"nom": "Synology", "logo_url": None, "description": "Serveurs NAS et solutions de stockage"},
    {"nom": "D-Link", "logo_url": None, "description": "Equipements réseaux pour particuliers et entreprises"},
    {"nom": "QNAP", "logo_url": None, "description": "Solutions NAS et stockage réseau"},
    {"nom": "Epson", "logo_url": None, "description": "Imprimantes, scanners et projection"},
    {"nom": "Brother", "logo_url": None, "description": "Imprimantes et périphériques"},
    {"nom": "Canon", "logo_url": None, "description": "Imprimantes, scanners, photo et vidéo"},
    {"nom": "Adobe", "logo_url": None, "description": "Logiciels créatifs et multimédia"},
    {"nom": "Acronis", "logo_url": None, "description": "Solutions de sauvegarde et sécurité"},
    {"nom": "3M", "logo_url": None, "description": "Accessoires technologiques et industriels"},
    {"nom": "Snom", "logo_url": None, "description": "Téléphonie IP professionnelle"},
    {"nom": "HyperX", "logo_url": None, "description": "Accessoires et matériels gaming"},
    {"nom": "LaCie", "logo_url": None, "description": "Solutions de stockage externes"},
    {"nom": "Sandisk", "logo_url": None, "description": "Cartes mémoire et stockage flash"},
    {"nom": "Bose", "logo_url": None, "description": "Audio professionnel et grand public"},
    {"nom": "Poly", "logo_url": None, "description": "Equipements audio et vidéo conférence"},
    {"nom": "Logitech G", "logo_url": None, "description": "Gamme gaming Logitech"},
    {"nom": "Anker", "logo_url": None, "description": "Accessoires mobiles et chargeurs"},
    {"nom": "NetApp", "logo_url": None, "description": "Solutions de stockage et serveurs"},
    {"nom": "Intel Optane", "logo_url": None, "description": "Technologie mémoire accélératrice"},
    {"nom": "TPV Technology", "logo_url": None, "description": "Fabricant d'écrans et téléviseurs"},
    {"nom": "Sony", "logo_url": None, "description": "Électronique grand public et professionnels"},
    {"nom": "Panasonic", "logo_url": None, "description": "Électronique et électroménager"},
    {"nom": "Toshiba", "logo_url": None, "description": "Multimédia et électronique"},
    {"nom": "AMD", "logo_url": None, "description": "Processeurs, GPU et semi-conducteurs"},
    {"nom": "Belkin", "logo_url": None, "description": "Accessoires réseau et mobiles"},
]

class Command(BaseCommand):
    help = 'Insère une liste prédéfinie de marques dans la base de données'

    def handle(self, *args, **options):
        for brand_data in BRANDS_DATA:
            brand, created = Brand.objects.get_or_create(
                nom=brand_data['nom'],
                defaults={'description': brand_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Marque créée : {brand.nom}'))
            else:
                self.stdout.write(f'Marque existe déjà : {brand.nom}')
        self.stdout.write(self.style.SUCCESS('Insertion des marques terminée.'))
