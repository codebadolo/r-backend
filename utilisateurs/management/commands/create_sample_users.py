import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utilisateurs.models import (
    ProfilEntreprise, ProfilParticulier, UserRole, Role
)

User = get_user_model()

ENTREPRISES = [
    # Nom, secteur, email, domaine
    ("Banque de l'Avenir",    "Banque",         "contact.banqueavenir@bf.com"),
    ("Banque du Faso",        "Banque",         "contact.banquefaso@bf.com"),
    ("Ministère Finances",    "Gouvernement",   "finance.ministere@bf.com"),
    ("Ministère Education",   "Gouvernement",   "education.ministere@bf.com"),
    ("Ministère Santé",       "Gouvernement",   "sante.ministere@bf.com"),
    ("SunTech Africa",        "Technologie",    "contact.suntech@bf.com"),
    ("Burkina IT Services",   "Technologie",    "info@burkina-it.bf"),
    ("Ouaga Innovation",      "Technologie",    "innovation@ouaga.bf"),
    ("Societé Agro Faso",     "Agroalimentaire","contact.agrofaso@bf.com"),
    ("Mobilis Logistics",     "Logistique",     "contact.logistics@bf.com"),
    ("BF Telecom",            "Télécom",        "info@bftelecom.bf"),
    ("Ouaga Clean",           "Services",       "info@ouagaclean.bf"),
    ("Burkina Santé Plus",    "Santé",          "santeplus@bf.com"),
    ("Burkina Energie",       "Énergie",        "info@energie.bf"),
    (" Faso Assurance",       "Assurance",      "contact.assurance@bf.com"),
    ("Ouaga Legal",           "Jurídique",      "contact.legal@bf.com"),
    ("Burkina Bâtiment",      "Construction",   "batiment@bf.com"),
    ("Transports Faso",       "Transport",      "contact.transport@bf.com"),
    ("Media Faso",            "Média",          "media@faso.bf"),
    ("Ouaga Finance Tech",    "Banque/Tech",    "finance.tech@ouaga.bf"),
]

PRENOMS = ["Abdoulaye", "Fatou", "Moussa", "Awa", "Idrissa", "Aminata", "Souleymane", "Marie", "Daouda", "Nafissatou",
           "Salif", "Adama", "Yaya", "Binta", "Souad", "Jonathan", "Nathan", "Isabelle", "Serge", "Carmen"]
NOMS = ["Ouedraogo", "Sawadogo", "Zongo", "Traoré", "Ilboudo", "Kaboré", "Kabore", "Sanou", "Kouanda", "Ouattara",
        "Kone", "Compaoré", "Kiema", "Bationo", "Bougma", "Yameogo", "Tapsoba", "Tiemtore", "Belem", "Kietega"]

DOMAINS = ["gmail.com", "yahoo.fr", "hotmail.com", "bfmail.com"]

ROLES_UTILS = ["SuperAdmin", "Manager", "OperateurLogistique", "ResponsableMarketing", "GestionnaireProduit"]


class Command(BaseCommand):
    help = "Crée 20 entreprises burkinabé et 40 utilisateurs particuliers (tous dans le back office) avec rôles différents"

    def handle(self, *args, **kwargs):
        # Création entreprise + profil
        for idx, (nom, secteur, email) in enumerate(ENTREPRISES, 1):
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": nom.split()[0],
                    "last_name": nom.split()[-1],
                    "type_client": "entreprise",
                    "accepte_cgv": True,
                    "is_active": True,
                }
            )
            ProfilEntreprise.objects.get_or_create(
                utilisateur=user,
                defaults={
                    "raison_sociale": nom,
                    "numero_siret": f"SIRET{random.randint(10000000, 99999999)}",
                    "numero_tva": f"BF{random.randint(100000,999999)}",
                    "adresse_societe": f"Ouagadougou Secteur {10+idx}, Burkina Faso",
                }
            )
            # Attribution d'un ou plusieurs rôles, au hasard
            n_roles = random.choice([1,2])
            roles = random.sample(list(Role.objects.all()), n_roles)
            for role in roles:
                UserRole.objects.get_or_create(user=user, role=role)
            self.stdout.write(self.style.SUCCESS(f"Entreprise créée: {nom} ({email}) — Rôles: {', '.join([r.name for r in roles])}"))

        # Création particuliers pour back-office
        for idx in range(40):
            first = random.choice(PRENOMS)
            last = random.choice(NOMS)
            email = f"{first.lower()}.{last.lower()}{random.randint(10, 99)}@{random.choice(DOMAINS)}"
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "first_name": first,
                    "last_name": last,
                    "type_client": "particulier",
                    "accepte_cgv": True,
                    "is_active": True,
                }
            )
            ProfilParticulier.objects.get_or_create(
                utilisateur=user,
                defaults={
                    "date_naissance": f"19{random.randint(75,99)}-{random.randint(1,12):02d}-{random.randint(1,28):02d}"
                }
            )
            # Attribution rôles
            n_roles = random.choice([1,2])
            roles = random.sample(list(Role.objects.all()), n_roles)
            for role in roles:
                UserRole.objects.get_or_create(user=user, role=role)
            self.stdout.write(self.style.SUCCESS(f"Particulier créé: {first} {last} ({email}) — Rôles: {', '.join([r.name for r in roles])}"))

        self.stdout.write(self.style.SUCCESS("Création massive de profils entreprise/particulier et rôles back-office terminée !"))
