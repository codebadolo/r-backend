from django.core.management.base import BaseCommand
from utilisateurs.models import Role, Permission, RolePermission

ROLES = [
    {
        "name": "SuperAdmin",
        "description": "Accès total à toutes les fonctionnalités du back-office"
    },
    {
        "name": "Manager",
        "description": "Gestion avancée des utilisateurs et contenus"
    },
    {
        "name": "OperateurLogistique",
        "description": "Gestion des commandes et livraisons"
    },
    {
        "name": "ResponsableMarketing",
        "description": "Gestion des campagnes marketing et newsletters"
    },
    {
        "name": "GestionnaireProduit",
        "description": "Ajout et modification des produits"
    },
    # Ajoute d'autres rôles selon besoin
]

PERMISSIONS = [
    {"code": "manage_users", "description": "Peut gérer les utilisateurs"},
    {"code": "manage_orders", "description": "Peut gérer les commandes"},
    {"code": "manage_products", "description": "Peut gérer les produits"},
    {"code": "manage_roles", "description": "Peut gérer les rôles"},
    {"code": "manage_logistics", "description": "Peut gérer la logistique"},
    {"code": "manage_marketing", "description": "Peut gérer les campagnes marketing"},
    # Ajoute d'autres permissions
]

# Pour associer permissions <-> rôle
ROLE_PERMISSIONS = {
    "SuperAdmin": ["manage_users", "manage_orders", "manage_products", "manage_roles", "manage_logistics", "manage_marketing"],
    "Manager":    ["manage_users", "manage_orders", "manage_products", "manage_marketing"],
    "OperateurLogistique": ["manage_orders", "manage_logistics"],
    "ResponsableMarketing": ["manage_marketing"],
    "GestionnaireProduit": ["manage_products"],
}


class Command(BaseCommand):
    help = "Crée les rôles et permissions de gestion du bac office"

    def handle(self, *args, **kwargs):
        # Création permissions
        perms = {}
        for perm_data in PERMISSIONS:
            perm, created = Permission.objects.get_or_create(code=perm_data["code"], defaults=perm_data)
            perms[perm.code] = perm
            self.stdout.write(self.style.SUCCESS(f"Permission: {perm.code} ({'créée' if created else 'existe'})"))
        
        # Création rôles
        roles = {}
        for role_data in ROLES:
            role, created = Role.objects.get_or_create(name=role_data["name"], defaults=role_data)
            roles[role.name] = role
            self.stdout.write(self.style.SUCCESS(f"Role: {role.name} ({'créé' if created else 'existe'})"))
        
        # Attribution des permissions aux rôles
        for role_name, perm_codes in ROLE_PERMISSIONS.items():
            role = roles[role_name]
            for code in perm_codes:
                perm = perms[code]
                RolePermission.objects.get_or_create(role=role, permission=perm)
                self.stdout.write(self.style.NOTICE(f"RolePermission: {role.name} -> {perm.code}"))

        self.stdout.write(self.style.SUCCESS("Rôles et permissions créés et liés avec succès."))
