from django.core.management.base import BaseCommand
from utilisateurs.models import User, Role, UserRole

class Command(BaseCommand):
    help = 'Créer des utilisateurs, rôles et associations initiales'

    def handle(self, *args, **options):
        # Création des rôles
        roles_data = [
            {'name': 'Admin Principal', 'description': 'Administrateur avec tous les droits'},
            {'name': 'Gestionnaire Produit', 'description': 'Gère les produits'},
            {'name': 'Support', 'description': 'Support client'},
            {'name': 'Client Standard', 'description': 'Client classique'},
        ]

        roles = {}
        for role_data in roles_data:
            role, created = Role.objects.get_or_create(name=role_data['name'], defaults={'description': role_data['description']})
            if created:
                self.stdout.write(self.style.SUCCESS(f"Rôle créé : {role.name}"))
            else:
                self.stdout.write(f"Rôle existant : {role.name}")
            roles[role.name] = role

        # Création des utilisateurs
        users_data = [
            {
                'email': 'admin@rohstore.com',
                'first_name': 'Alice',
                'last_name': 'Dupont',
                'password': 'adminpassword',
                'is_staff': True,
                'is_superuser': True,
                'roles': ['Admin Principal'],
            },
            {
                'email': 'gestionnaire@rohstore.com',
                'first_name': 'Mamadou',
                'last_name': 'Sarr',
                'password': 'gestionpassword',
                'is_staff': True,
                'roles': ['Gestionnaire Produit', 'Support'],
            },
            {
                'email': 'client1@example.com',
                'first_name': 'Fatou',
                'last_name': 'Diop',
                'password': 'clientpassword',
                'roles': ['Client Standard'],
            },
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(email=user_data['email'])
            if created:
                user.first_name = user_data['first_name']
                user.last_name = user_data['last_name']
                user.is_staff = user_data.get('is_staff', False)
                user.is_superuser = user_data.get('is_superuser', False)
                user.set_password(user_data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Utilisateur créé : {user.email}"))
            else:
                self.stdout.write(f"Utilisateur existant : {user.email}")

            # Associer les rôles
            for role_name in user_data.get('roles', []):
                role = roles.get(role_name)
                if role:
                    user_role, ur_created = UserRole.objects.get_or_create(user=user, role=role)
                    if ur_created:
                        self.stdout.write(self.style.SUCCESS(f"Rôle '{role_name}' assigné à {user.email}"))
                    else:
                        self.stdout.write(f"Rôle '{role_name}' déjà assigné à {user.email}")

        self.stdout.write(self.style.SUCCESS("Création initiale terminée."))
