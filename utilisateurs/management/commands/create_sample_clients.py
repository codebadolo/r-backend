import random
import re
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utilisateurs.models import (
    Adresse,
    Role,
    Permission,
    RolePermission,
    Pays,
    FormeJuridique,
    RegimeFiscal,
    DivisionFiscale,
    UserTVANumber,
)

User = get_user_model()

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
]

RAISONS_SOCIALES = [
    "Société Générale", "ABC Industries", "Compagnie Tertiaire", "Groupe Ouaga", "MaliTech",
    "Sarl Benin Services", "Togo Logistics", "Senegal Export", "Ivory Trade",
    "Guinée Agro", "Cap-Vert Solutions", "Libéria Finance", "Sierra Leone Invest",
]

RESPONSABLES = [
    "Kofi Mensah", "Awa Diop", "Moussa Traoré", "Fatoumata Coulibaly", "Issa Konaté",
    "Aminata Diallo", "Oumar Sanogo", "Salif Bah", "Mariam Sow", "Souleymane Cissé"
]

ROLE_ENTREPRISE_NAME = "ClientEntreprise"
DEFAULT_PASSWORD = "Entrepris3@123"

ROLES = [
    {"name": ROLE_ENTREPRISE_NAME, "description": "Utilisateur client entreprise"},
]

PERMISSIONS = [
    {"code": "view_products", "description": "Peut voir les produits"},
    {"code": "make_orders", "description": "Peut passer des commandes"},
]

ROLE_PERMISSIONS = {
    ROLE_ENTREPRISE_NAME: ["view_products", "make_orders"],
}

VILLES_PAR_PAYS = {
    "Burkina Faso": ["Ouagadougou", "Bobo-Dioulasso", "Koudougou"],
    "Niger": ["Niamey", "Zinder", "Maradi"],
    "Mali": ["Bamako", "Kayes", "Sikasso"],
    "Bénin": ["Cotonou", "Porto-Novo", "Parakou"],
    "Togo": ["Lomé", "Sokodé", "Kara"],
    "Sénégal": ["Dakar", "Thiès", "Saint-Louis"],
    "Côte d'Ivoire": ["Abidjan", "Bouaké", "Yamoussoukro"],
    "Guinée": ["Conakry", "Nzérékoré", "Kankan"],
    "Cap-Vert": ["Praia", "Mindelo"],
    "Gambie": ["Banjul", "Serrekunda"],
    "Libéria": ["Monrovia", "Gbarnga"],
    "Sierra Leone": ["Freetown", "Bo"],
}

class Command(BaseCommand):
    help = "Créer 20 clients entreprises avec adresses facturation/livraison distinctes et numéros TVA"

    def normalize_str(self, s):
        s = s.lower()
        s = re.sub(r'[^\w\s-]', '', s)
        s = re.sub(r'[\s-]+', '.', s)
        return s

    def handle(self, *args, **kwargs):
        # 1. Créer ou récupérer permissions
        permissions_map = {}
        for perm_data in PERMISSIONS:
            perm, created = Permission.objects.get_or_create(
                code=perm_data["code"],
                defaults={"description": perm_data["description"]},
            )
            permissions_map[perm.code] = perm
            self.stdout.write(self.style.SUCCESS(f"Permission créée : {perm.code}") if created else f"Permission existante : {perm.code}")

        # 2. Créer ou récupérer rôles
        roles_map = {}
        for role_data in ROLES:
            role, created = Role.objects.get_or_create(
                name=role_data["name"],
                defaults={"description": role_data["description"]},
            )
            roles_map[role.name] = role
            self.stdout.write(self.style.SUCCESS(f"Rôle créé : {role.name}") if created else f"Rôle existant : {role.name}")
        
        # 3. Associer rôles & permissions
        for role_name, perm_codes in ROLE_PERMISSIONS.items():
            role = roles_map.get(role_name)
            if not role:
                self.stderr.write(f"Rôle '{role_name}' introuvable, association ignorée.")
                continue

            RolePermission.objects.filter(role=role).delete()
            for code in perm_codes:
                perm = permissions_map.get(code)
                if not perm:
                    self.stderr.write(f"Permission '{code}' introuvable, ignorée.")
                    continue
                RolePermission.objects.get_or_create(role=role, permission=perm)
            self.stdout.write(f"Permissions associées au rôle : {role_name}")

        # 4. Charger tables référentielles
        from utilisateurs.models import FormeJuridique, RegimeFiscal, DivisionFiscale
        formes_juridiques = list(FormeJuridique.objects.all())
        regimes_fiscaux = list(RegimeFiscal.objects.all())
        divisions_fiscales = list(DivisionFiscale.objects.all())

        if not formes_juridiques or not regimes_fiscaux or not divisions_fiscales:
            self.stderr.write("Remplissez FormeJuridique, RegimeFiscal, DivisionFiscale avant d'exécuter.")
            return

        # 5. Créer 20 utilisateurs
        for i in range(20):
            pays_data = random.choice(PAYS)
            try:
                pays_obj = Pays.objects.get(nom__iexact=pays_data["nom"])
            except Pays.DoesNotExist:
                self.stderr.write(f"Pays '{pays_data['nom']}' inconnu en base, utilisateur ignoré.")
                continue

            raison_sociale = random.choice(RAISONS_SOCIALES) + f" #{i+1}"
            nom_responsable = random.choice(RESPONSABLES)

            prenom_nom = self.normalize_str(nom_responsable.replace(" ", "."))
            raison_sociale_norm = self.normalize_str(raison_sociale)
            email = f"{prenom_nom}.{raison_sociale_norm}.{i}@example.com"

            User.objects.filter(email=email).delete()

            user = User.objects.create_user(
                email=email,
                password=DEFAULT_PASSWORD,
                type_client="entreprise",
            )
            self.stdout.write(f"Création utilisateur entreprise: {raison_sociale} ({email})")

            adresse_facturation = Adresse.objects.create(
                utilisateur=user,
                utilisation="facturation",
                type_client="entreprise",
                nom_complet=nom_responsable,
                telephone=f"{pays_data['code_telephone']} {random.randint(60000000, 89999999)}",
                pays=pays_obj,
                rue="Avenue des Nations",
                numero=str(random.randint(1, 200)),
                ville=random.choice(VILLES_PAR_PAYS.get(pays_obj.nom, ["Villeprincipale"])),
                code_postal=str(random.randint(1000, 9999)),

                raison_sociale=raison_sociale,
                rccm=f"RCCM-{random.randint(1000000, 9999999)}",
                ifu=f"IFU{random.randint(1000000000, 9999999999)}",
                forme_juridique=random.choice(formes_juridiques),
                regime_fiscal=random.choice(regimes_fiscaux),
                division_fiscale=random.choice(divisions_fiscales),
                livraison_identique_facturation=True,
            )
            self.stdout.write(f"  Adresse facturation créée: {adresse_facturation.rue} {adresse_facturation.numero}, {adresse_facturation.ville}, {adresse_facturation.pays.nom}")

            # 50% des cas, adresse livraison différente
            if random.random() < 0.5:
                adresse_livraison = Adresse.objects.create(
                    utilisateur=user,
                    utilisation="livraison",
                    type_client="entreprise",
                    nom_complet=nom_responsable,
                    telephone=f"{pays_data['code_telephone']} {random.randint(60000000, 89999999)}",
                    pays=pays_obj,
                    rue="Rue de la Liberté",
                    numero=str(random.randint(1, 200)),
                    ville=random.choice(VILLES_PAR_PAYS.get(pays_obj.nom, ["Villeprincipale"])),
                    code_postal=str(random.randint(1000, 9999)),

                    raison_sociale=raison_sociale,
                    rccm=adresse_facturation.rccm,
                    ifu=adresse_facturation.ifu,
                    forme_juridique=adresse_facturation.forme_juridique,
                    regime_fiscal=adresse_facturation.regime_fiscal,
                    division_fiscale=adresse_facturation.division_fiscale,
                    livraison_identique_facturation=False,
                )
                self.stdout.write(f"  Adresse livraison différente créée: {adresse_livraison.rue} {adresse_livraison.numero}, {adresse_livraison.ville}, {adresse_livraison.pays.nom}")
            else:
                adresse_facturation.livraison_identique_facturation = True
                adresse_facturation.save()
                self.stdout.write("  Adresse livraison identique à l'adresse facturation.")

            # Création de 1 à 3 numéros TVA
            nb_tva = random.randint(1, 3)
            for _ in range(nb_tva):
                numero = f"TVA{random.randint(1000000000, 9999999999)}"
                UserTVANumber.objects.create(
                    utilisateur=user,
                    numero_tva=numero,
                    pays=pays_obj.nom,
                )
                self.stdout.write(f"  Numéro TVA ajouté: {numero} ({pays_obj.nom})")

            role_entreprise = roles_map.get(ROLE_ENTREPRISE_NAME)
            if role_entreprise:
                user.roles.add(role_entreprise)
                self.stdout.write(f"  Rôle '{role_entreprise.name}' assigné à l'utilisateur.")
            else:
                self.stderr.write(f"Rôle '{ROLE_ENTREPRISE_NAME}' introuvable, non assigné.")

        self.stdout.write(self.style.SUCCESS("Création de 20 utilisateurs entreprises terminée."))
