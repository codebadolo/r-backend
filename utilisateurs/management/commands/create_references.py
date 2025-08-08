from django.core.management.base import BaseCommand
from utilisateurs.models import Pays, RegimeFiscal, FormeJuridique, DivisionFiscale

# Données à insérer (exemple listes basiques)
PAYS = [
    {"nom": "Burkina Faso", "code_telephone": "+226"},
    {"nom": "Niger", "code_telephone": "+227"},
    {"nom": "Mali", "code_telephone": "+223"},
    {"nom": "Bénin", "code_telephone": "+229"},
    {"nom": "Togo", "code_telephone": "+228"},
    {"nom": "Sénégal", "code_telephone": "+221"},
    {"nom": "Côte d'Ivoire", "code_telephone": "+225"},
    {"nom": "Guinée", "code_telephone": "+224"},
    {"nom": "Cap-Vert", "code_telephone": "+238"},
    {"nom": "Gambie", "code_telephone": "+220"},
    {"nom": "Libéria", "code_telephone": "+231"},
    {"nom": "Sierra Leone", "code_telephone": "+232"},
    # Ajoutez d’autres pays de la sous-région ouest-africaine si besoin
]

REGIMES_FISCAUX = [
    {"nom": "Régime réel normal"},
    {"nom": "Régime simplifié"},
    {"nom": "Régime forfaitaire"},
    {"nom": "Régime de la micro-entreprise"},
    {"nom": "Régime de l’auto-entrepreneur"},
    # Vous pouvez rajouter des régimes spécifiques au contexte local
]

FORMES_JURIDIQUES = [
    {"nom": "SARL"},                 # Société à responsabilité limitée
    {"nom": "SA"},                  # Société anonyme
    {"nom": "SAS"},                 # Société par actions simplifiée
    {"nom": "Entreprise Individuelle"},
    {"nom": "SNC"},                 # Société en nom collectif
    {"nom": "Société Coopérative"},
    {"nom": "Groupement d’intérêt économique"},
    # Etc. selon les formes juridiques admises localement
]

DIVISIONS_FISCALES = [
    {"nom": "Ouaga I"},
    {"nom": "Ouaga II"},
    {"nom": "Ouaga III"},
    {"nom": "Bobo-Dioulasso"},
    {"nom": "Koudougou"},
    {"nom": "Ouahigouya"},
    {"nom": "Fada N’Gourma"},
    {"nom": "Banfora"},
    # Ajoutez les divisions administratives/fiscales pertinentes
]

class Command(BaseCommand):
    help = 'Crée les pays, régimes fiscaux, formes juridiques et divisions fiscales par défaut.'

    def handle(self, *args, **options):
        # création pays
        for p in PAYS:
            obj, created = Pays.objects.get_or_create(nom=p['nom'], defaults={"code_telephone": p['code_telephone']})
            action = "Créé" if created else "Existe déjà"
            self.stdout.write(f"{action} pays : {obj.nom}")

        # création régimes fiscaux
        for r in REGIMES_FISCAUX:
            obj, created = RegimeFiscal.objects.get_or_create(nom=r['nom'])
            action = "Créé" if created else "Existe déjà"
            self.stdout.write(f"{action} régime fiscal : {obj.nom}")

        # création formes juridiques
        for f in FORMES_JURIDIQUES:
            obj, created = FormeJuridique.objects.get_or_create(nom=f['nom'])
            action = "Créé" if created else "Existe déjà"
            self.stdout.write(f"{action} forme juridique : {obj.nom}")

        # création divisions fiscales
        for d in DIVISIONS_FISCALES:
            obj, created = DivisionFiscale.objects.get_or_create(nom=d['nom'])
            action = "Créé" if created else "Existe déjà"
            self.stdout.write(f"{action} division fiscale : {obj.nom}")

        self.stdout.write(self.style.SUCCESS("Références initiales créées avec succès."))
