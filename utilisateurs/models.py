from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


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


class User(AbstractBaseUser, PermissionsMixin):
    TYPE_CLIENT_CHOIX = [
        ('particulier', 'Particulier'),
        ('entreprise', 'Entreprise'),
    ]

    email = models.EmailField(unique=True)
    type_client = models.CharField(max_length=20, choices=TYPE_CLIENT_CHOIX, default='particulier')
    # Remarque : mot de passe géré via AbstractBaseUser (hashed + salt), pas besoin de champ supplémentaire ici
    # Les noms fusionnés dans profils (voir plus bas)

    accepte_facture_electronique = models.BooleanField(default=False)
    accepte_cgv = models.BooleanField(default=False)
    telephone = models.CharField(max_length=20, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class UserTVANumber(models.Model):
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='numero_tva_valides')
    numero_tva = models.CharField(max_length=30)
    pays = models.CharField(max_length=100)
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'numero_tva')

    def __str__(self):
        return f"{self.numero_tva} ({self.pays})"

class FormeJuridique(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class RegimeFiscal(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class DivisionFiscale(models.Model):
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class Pays(models.Model):
    nom = models.CharField(max_length=100)
    code_telephone = models.CharField(max_length=10)  # Exemple : '+226' pour Burkina Faso

    def __str__(self):
        return self.nom

class Adresse(models.Model):
    UTILISATION_CHOIX = [
        ('facturation', 'Facturation'),
        ('livraison', 'Livraison'),
    ]

    TYPE_CLIENT_CHOIX = [
        ('particulier', 'Particulier'),
        ('entreprise', 'Entreprise'),
    ]

    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adresses')
    utilisation = models.CharField(max_length=20, choices=UTILISATION_CHOIX)
    type_client = models.CharField(max_length=20, choices=TYPE_CLIENT_CHOIX, default='particulier')

    nom_complet = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20)
    raison_sociale = models.CharField(max_length=255, blank=True, null=True)  # Remplit si entreprise

    numero_tva = models.ForeignKey(UserTVANumber, on_delete=models.SET_NULL, blank=True, null=True, related_name='adresses')

    pays = models.ForeignKey(Pays, on_delete=models.PROTECT)
    forme_juridique = models.ForeignKey(FormeJuridique, null=True, blank=True, on_delete=models.SET_NULL)
    regime_fiscal = models.ForeignKey(RegimeFiscal, null=True, blank=True, on_delete=models.SET_NULL)
    division_fiscale = models.ForeignKey(DivisionFiscale, null=True, blank=True, on_delete=models.SET_NULL)

    rccm = models.CharField(max_length=100, blank=True, null=True)
    ifu = models.CharField(max_length=100, blank=True, null=True)
    rue = models.CharField(max_length=255)
    numero = models.CharField(max_length=10, blank=True, null=True)

    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
 

    livraison_identique_facturation = models.BooleanField(default=False)  # Par exemple, pour gérer ce flag en adresse

    def __str__(self):
        return f"{self.nom_complet} - {self.rue} {self.numero or ''}, {self.ville}"





# Rôles, permissions, historiques (inchangé par rapport à votre base)
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
