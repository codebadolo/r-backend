import random
import re
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utilisateurs.models import (
    Adresse,
    Role,
    Permission,
    RolePermission,
    UserRole,
    Pays,
    FormeJuridique,
    RegimeFiscal,
    DivisionFiscale,
)

User = get_user_model()

# Liste des pays avec codes téléphoniques (doivent exister en base!)
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

# Exemples de raisons sociales et noms d'entreprises (à personnaliser)
RAISONS_SOCIALES = [
    "Société Générale", "ABC Industries", "Compagnie Tertiaire", "Groupe Ouaga", "MaliTech",
    "Sarl Benin Services", "Togo Logistics", "Senegal Export", "Ivory Trade",
    "Guinée Agro", "Cap-Vert Solutions", "Libéria Finance", "Sierra Leone Invest",
]

# Listes typiques pour noms responsables, formes juridiques, régimes fiscaux, divisions fiscales
RESPONSABLES = [
    "Kofi Mensah", "Awa Diop", "Moussa Traoré", "Fatoumata Coulibaly", "Issa Konaté",
    "Aminata Diallo", "Oumar Sanogo", "Salif Bah", "Mariam Sow", "Souleymane Cissé"
]

# Ces tables doivent être préremplies en base
FORMES_JURIDIQUES = []
REGIMES_FISCAUX = []
DIVISIONS_FISCALES = []

# Rôle à assigner
ROLE_ENTREPRISE_NAME = "ClientEntreprise"

# Mot de passe par défaut
DEFAULT_PASSWORD = "Entrepris3@123"

# Permissions et rôles (pour création ou récupération)
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

# Villes typiques par pays (exemple partiel, adapter selon pays)
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
    help = "Créer 20 clients entreprises divers selon plusieurs pays avec adresses complètes et emails basés sur nom & raison sociale."

    def normalize_str(self, s):
        """Transforme une chaîne en format email-friendly (lowercase, points pour espaces/tiret, suppression caractères spéciaux)."""
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
                defaults={"description": perm_data["description"]}
            )
            permissions_map[perm.code] = perm
            if created:
                self.stdout.write(self.style.SUCCESS(f"Permission créée : {perm.code}"))
            else:
                self.stdout.write(f"Permission existante : {perm.code}")

        # 2. Créer ou récupérer rôles
        roles_map = {}
        for role_data in ROLES:
            role, created = Role.objects.get_or_create(
                name=role_data["name"],
                defaults={"description": role_data["description"]}
            )
            roles_map[role.name] = role
            if created:
                self.stdout.write(self.style.SUCCESS(f"Rôle créé : {role.name}"))
            else:
                self.stdout.write(f"Rôle existant : {role.name}")

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

        # 4. Charger les tables référentielles FormeJuridique, RegimeFiscal, DivisionFiscale en DB
        global FORMES_JURIDIQUES, REGIMES_FISCAUX, DIVISIONS_FISCALES
        FORMES_JURIDIQUES = list(FormeJuridique.objects.all())
        REGIMES_FISCAUX = list(RegimeFiscal.objects.all())
        DIVISIONS_FISCALES = list(DivisionFiscale.objects.all())

        if not FORMES_JURIDIQUES or not REGIMES_FISCAUX or not DIVISIONS_FISCALES:
            self.stderr.write("Merci de remplir les tables FormeJuridique, RegimeFiscal et DivisionFiscale avant d'exécuter cette commande.")
            return

        # 5. Créer 20 utilisateurs entreprise
        for i in range(20):
            # Choisir pays aléatoire et objet Pays existant
            pays_data = random.choice(PAYS)
            try:
                pays_obj = Pays.objects.get(nom__iexact=pays_data["nom"])
            except Pays.DoesNotExist:
                self.stderr.write(f"Pays '{pays_data['nom']}' absent en base, utilisateur ignoré.")
                continue

            raison_sociale = random.choice(RAISONS_SOCIALES) + f" #{i+1}"
            nom_responsable = random.choice(RESPONSABLES)

            # Générer email basé sur nom_responsable + raison_sociale + index
            prenom_nom = self.normalize_str(nom_responsable.replace(" ", "."))
            raison_sociale_norm = self.normalize_str(raison_sociale)
            email = f"{prenom_nom}.{raison_sociale_norm}.{i}@example.com"

            # Supprimer utilisateur existant s'il y en a
            User.objects.filter(email=email).delete()

            # Création utilisateur type entreprise
            user = User.objects.create_user(
                email=email,
                password=DEFAULT_PASSWORD,
                type_client="entreprise",
            )
            self.stdout.write(f"Création utilisateur entreprise: {raison_sociale} ({email})")

            # Création adresse complète entreprise avec tous les champs
            adresse = Adresse.objects.create(
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
                forme_juridique=random.choice(FORMES_JURIDIQUES),
                regime_fiscal=random.choice(REGIMES_FISCAUX),
                division_fiscale=random.choice(DIVISIONS_FISCALES),

                livraison_identique_facturation=True,
            )
            self.stdout.write(f"  Adresse créée: {adresse.rue} {adresse.numero}, {adresse.ville}, {adresse.pays.nom}")

            # Assignation du rôle entreprise
            role_entreprise = roles_map.get(ROLE_ENTREPRISE_NAME)
            if role_entreprise:
                UserRole.objects.create(user=user, role=role_entreprise)
                self.stdout.write(f"  Rôle '{role_entreprise.name}' assigné à l'utilisateur.")
            else:
                self.stderr.write(f"Rôle '{ROLE_ENTREPRISE_NAME}' introuvable, non assigné.")

        self.stdout.write(self.style.SUCCESS("Création de 20 utilisateurs entreprises terminée."))
