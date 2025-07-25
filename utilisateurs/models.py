from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


# Gestionnaire personnalisé utilisateur (à garder)
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('L\'adresse email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Le superuser doit avoir is_superuser=True.')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Le superuser doit avoir is_staff=True.')
        return self.create_user(email, password, **extra_fields)


# Modèle utilisateur personnalisé
class User(AbstractBaseUser, PermissionsMixin):
    TYPE_CLIENT_CHOIX = [
        ('particulier', 'Particulier'),
        ('entreprise', 'Entreprise'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    type_client = models.CharField(max_length=20, choices=TYPE_CLIENT_CHOIX, default='particulier')
    accepte_facture_electronique = models.BooleanField(default=False)
    accepte_cgv = models.BooleanField(default=False)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email


# Modèle pour stocker les numéros TVA validés pour un utilisateur
class UserTVANumber(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='numero_tva_valides')
    numero_tva = models.CharField(max_length=30)
    pays = models.CharField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'numero_tva')

    def __str__(self):
        return f"{self.numero_tva} ({self.pays})"


# Modèle Adresse avec numéro TVA sous forme de clé étrangère vers UserTVANumber
class Adresse(models.Model):
    UTILISATION_CHOIX = [
        ('facturation', 'Facturation'),
        ('livraison', 'Livraison'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adresses')
    utilisation = models.CharField(max_length=20, choices=UTILISATION_CHOIX)
    nom_complet = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    raison_sociale = models.CharField(max_length=255, blank=True, null=True)
    numero_siret = models.CharField(max_length=20, blank=True, null=True)
    numero_tva = models.ForeignKey(UserTVANumber, on_delete=models.SET_NULL, blank=True, null=True, related_name='adresses')  # << ici le lien vers les numéros TVA validés par l'utilisateur

    rue = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complement = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
    pays = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nom_complet} - {self.rue} {self.numero}, {self.ville}"


# Profils et rôles (à garder selon besoins précédents)

class ProfilEntreprise(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_entreprise')
    raison_sociale = models.CharField(max_length=255)
    numero_siret = models.CharField(max_length=20, blank=True, null=True)
    numero_tva = models.CharField(max_length=30, blank=True, null=True)  # peut être redondant mais utile pour rapide accès
    adresse_societe = models.CharField(max_length=255, blank=True, null=True)
    telephone_suppl = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Profil entreprise {self.raison_sociale} - {self.utilisateur.email}"


class ProfilParticulier(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_particulier')
    date_naissance = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"Profil particulier {self.utilisateur.email}"


class Role(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class UserRole(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_roles')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_users')
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'role')

    def __str__(self):
        return f"{self.user.email} - {self.role.name}"


class Permission(models.Model):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class RolePermission(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='role_permissions')
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE, related_name='permission_roles')

    class Meta:
        unique_together = ('role', 'permission')

    def __str__(self):
        return f"{self.role.name} - {self.permission.code}"


class HistoriqueConnexion(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='historiques_connexion')
    adresse_ip = models.GenericIPAddressField(blank=True, null=True)
    date_connexion = models.DateTimeField(auto_now_add=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Connexion {self.utilisateur.email} le {self.date_connexion}"
