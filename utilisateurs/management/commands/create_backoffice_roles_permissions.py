from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from utilisateurs.models import Role, UserRole  # Adaptez selon votre app

User = get_user_model()

# Liste des utilisateurs back-office à créer avec les rôles à leur assigner
USERS_DATA = [
    {
        "email": "admin@example.com",
        "password": "password123",
        "roles": ["SuperAdmin", "Manager"]
    },
    {
        "email": "manager@example.com",
        "password": "password123",
        "roles": ["Manager"]
    },
    {
        "email": "logistique@example.com",
        "password": "password123",
        "roles": ["OperateurLogistique"]
    },
    {
        "email": "marketing@example.com",
        "password": "password123",
        "roles": ["ResponsableMarketing"]
    },
    {
        "email": "produits@example.com",
        "password": "password123",
        "roles": ["GestionnaireProduit"]
    },
]

class Command(BaseCommand):
    help = "Créer uniquement des utilisateurs back-office et leur assigner des rôles existants."

    def handle(self, *args, **kwargs):
        for user_data in USERS_DATA:
            email = user_data["email"]
            password = user_data["password"]
            role_names = user_data.get("roles", [])

            # Supprimer l'utilisateur s'il existe déjà (pour recréer proprement)
            User.objects.filter(email=email).delete()

            # Création de l'utilisateur (adaptez selon vos champs requis)
            user = User.objects.create_user(email=email, password=password, type_client='particulier')

            # Assignation des rôles existants
            for role_name in role_names:
                try:
                    role = Role.objects.get(name=role_name)
                except Role.DoesNotExist:
                    self.stderr.write(f"Rôle '{role_name}' non trouvé en base, non assigné à {email}")
                    continue

                UserRole.objects.create(user=user, role=role)
                self.stdout.write(f"Rôle '{role_name}' assigné à {email}")

            self.stdout.write(self.style.SUCCESS(f"Utilisateur créé : {email} avec rôles {role_names}"))

        self.stdout.write(self.style.SUCCESS("Création des utilisateurs back-office terminée."))
