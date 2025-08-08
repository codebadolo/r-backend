from django.core.management.base import BaseCommand
from utilisateurs.models import Role, Permission, RolePermission

ROLES = [
    {"name": "SuperAdmin", "description": "Accès total à toutes les fonctionnalités du back-office"},
    {"name": "Manager", "description": "Gestion avancée des utilisateurs et contenus"},
    {"name": "OperateurLogistique", "description": "Gestion des commandes et livraisons"},
    {"name": "ResponsableMarketing", "description": "Gestion des campagnes marketing et newsletters"},
    {"name": "GestionnaireProduit", "description": "Ajout et modification des produits"},
]

PERMISSIONS = [
    {"code": "manage_users", "description": "Peut gérer les utilisateurs"},
    {"code": "manage_orders", "description": "Peut gérer les commandes"},
    {"code": "manage_products", "description": "Peut gérer les produits"},
    {"code": "manage_roles", "description": "Peut gérer les rôles"},
    {"code": "manage_logistics", "description": "Peut gérer la logistique"},
    {"code": "manage_marketing", "description": "Peut gérer les campagnes marketing"},
]

ROLE_PERMISSIONS = {
    "SuperAdmin": ["manage_users", "manage_orders", "manage_products", "manage_roles", "manage_logistics", "manage_marketing"],
    "Manager": ["manage_users", "manage_orders", "manage_products", "manage_marketing"],
    "OperateurLogistique": ["manage_orders", "manage_logistics"],
    "ResponsableMarketing": ["manage_marketing"],
    "GestionnaireProduit": ["manage_products"],
}

class Command(BaseCommand):
    help = "Créer les rôles, permissions et leurs associations via RolePermission."

    def handle(self, *args, **options):
        # Création des permissions
        perm_objs = {}
        for perm in PERMISSIONS:
            p, created = Permission.objects.get_or_create(code=perm["code"], defaults={"description": perm["description"]})
            perm_objs[perm["code"]] = p
            self.stdout.write(f'{"Créée" if created else "Existe déjà"} permission : {p.code}')

        # Création des rôles
        for role_data in ROLES:
            role, created = Role.objects.get_or_create(name=role_data["name"], defaults={"description": role_data["description"]})
            self.stdout.write(f'{"Créé" if created else "Existe déjà"} rôle : {role.name}')

            # Supprimer les anciennes associations
            RolePermission.objects.filter(role=role).delete()

            # Créer les nouvelles associations RolePermission
            for perm_code in ROLE_PERMISSIONS.get(role.name, []):
                perm = perm_objs.get(perm_code)
                if perm:
                    RolePermission.objects.get_or_create(role=role, permission=perm)
            self.stdout.write(f'Permissions associées au rôle : {role.name}')

        self.stdout.write(self.style.SUCCESS("Rôles et permissions créés et associés avec succès."))
