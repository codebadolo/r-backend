import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utilisateurs.models import Adresse, Role, Permission, RolePermission, UserRole, Pays

User = get_user_model()

# Listes simplifiées de prénoms et noms typiques BF/sous-région
PRENOMS = [
    "Issa", "Fatoumata", "Abdoulaye", "Awa", "Moussa", "Aminata", "Souleymane",
    "Halima", "Yacouba", "Salif", "Mariam", "Oumar", "Adama", "Zeinabou",
]

NOMS = [
    "Ouédraogo", "Sankara", "Zongo", "Traoré", "Diallo", "Konaté", "Coulibaly",
    "Barry", "Diarra", "Cissé", "Kaboré", "Sawadogo", "Sanon",
]

VILLES_BF = [
    "Ouagadougou", "Bobo-Dioulasso", "Koudougou", "Banfora", "Ouahigouya", "Fada N’Gourma"
]

PAYS_BF_NAME = "Burkina Faso"

# Rôles et permissions à créer ou récupérer
ROLES = [
    {"name": "ClientParticulier", "description": "Utilisateur particulier client"},
    # Ajoutez d'autres rôles si nécessaire
]

PERMISSIONS = [
    {"code": "view_products", "description": "Peut voir les produits"},
    {"code": "make_orders", "description": "Peut passer des commandes"},
    # Ajoutez d'autres permissions pertinentes
]

ROLE_PERMISSIONS = {
    "ClientParticulier": ["view_products", "make_orders"],
}

# Mot de passe par défaut pour les comptes de test
DEFAULT_PASSWORD = "Test@1234"

class Command(BaseCommand):
    help = "Créer les rôles, permissions et 20 utilisateurs particuliers Burkina Faso avec adresses et rôles."

    def handle(self, *args, **kwargs):
        # 1. Créer ou récupérer les permissions
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

        # 2. Créer ou récupérer les rôles
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

        # 3. Associer rôles et permissions via RolePermission
        for role_name, perm_codes in ROLE_PERMISSIONS.items():
            role = roles_map.get(role_name)
            if not role:
                self.stderr.write(f"Rôle '{role_name}' introuvable, association ignorée.")
                continue

            # Supprimer anciennes associations
            RolePermission.objects.filter(role=role).delete()

            for code in perm_codes:
                perm = permissions_map.get(code)
                if not perm:
                    self.stderr.write(f"Permission '{code}' introuvable, ignorée.")
                    continue
                RolePermission.objects.get_or_create(role=role, permission=perm)
            self.stdout.write(f"Permissions associées au rôle : {role_name}")

        # 4. Récupérer le pays Burkina Faso
        try:
            pays_bf = Pays.objects.get(nom__iexact=PAYS_BF_NAME)
        except Pays.DoesNotExist:
            self.stderr.write(f"Pays '{PAYS_BF_NAME}' non trouvé. Veuillez le créer avant de lancer cette commande.")
            return

        # 5. Créer les 20 utilisateurs particuliers
        role_particulier = roles_map.get("ClientParticulier")
        if not role_particulier:
            self.stderr.write("Le rôle 'ClientParticulier' est introuvable. Abandon de la création d'utilisateurs.")
            return

        for i in range(20):
            prenom = random.choice(PRENOMS)
            nom = random.choice(NOMS)
            nom_complet = f"{prenom} {nom}"

            email = f"{prenom.lower()}.{nom.lower()}{i}@example.com"

            # Supprimer l'utilisateur existant
            User.objects.filter(email=email).delete()

            # Création utilisateur
            user = User.objects.create_user(
                email=email,
                password=DEFAULT_PASSWORD,
                type_client="particulier",
            )
            self.stdout.write(f"Création utilisateur: {nom_complet} ({email})")

            # Création adresse liée
            adresse = Adresse.objects.create(
                utilisateur=user,
                utilisation="facturation",
                type_client="particulier",
                nom_complet=nom_complet,
                telephone=f"+226 {random.randint(60000000, 79999999)}",
                pays=pays_bf,
                rue="Rue de l'Indépendance",
                numero=str(random.randint(1, 100)),
                ville=random.choice(VILLES_BF),
                code_postal=str(random.randint(7000, 8000)),
                livraison_identique_facturation=True,
            )
            self.stdout.write(f"  Adresse créée: {adresse.rue} {adresse.numero}, {adresse.ville}, {adresse.pays.nom}")

            # Association rôle utilisateur
            UserRole.objects.create(user=user, role=role_particulier)
            self.stdout.write(f"  Rôle '{role_particulier.name}' assigné à l'utilisateur.")

        self.stdout.write(self.style.SUCCESS("Création de 20 utilisateurs particuliers terminée."))
