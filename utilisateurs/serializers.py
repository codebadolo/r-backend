from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import (
    Adresse,
    Role, Permission, RolePermission,
    UserTVANumber, HistoriqueConnexion , Pays, FormeJuridique, RegimeFiscal ,DivisionFiscale
)

User = get_user_model()


class UserTVANumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTVANumber
        fields = ['id', 'numero_tva', 'pays', 'date_ajout']

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ['id', 'nom', 'code_telephone']

class FormeJuridiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormeJuridique
        fields = ['id', 'nom']

class RegimeFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegimeFiscal
        fields = ['id', 'nom']

class DivisionFiscaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivisionFiscale
        fields = ['id', 'nom']

'''class AdresseSerializer(serializers.ModelSerializer):
    # Relations en lecture (détail complet)
    pays = PaysSerializer(read_only=True)
    forme_juridique = FormeJuridiqueSerializer(read_only=True)
    regime_fiscal = RegimeFiscalSerializer(read_only=True)
    division_fiscale = DivisionFiscaleSerializer(read_only=True)
    numero_tva = UserTVANumberSerializer(read_only=True)

    # Relations en écriture (via ID uniquement)
    pays_id = serializers.PrimaryKeyRelatedField(
        source='pays',
        queryset=Pays.objects.all(),
        write_only=True
    )
    forme_juridique_id = serializers.PrimaryKeyRelatedField(
        source='forme_juridique',
        queryset=FormeJuridique.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )
    regime_fiscal_id = serializers.PrimaryKeyRelatedField(
        source='regime_fiscal',
        queryset=RegimeFiscal.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )
    division_fiscale_id = serializers.PrimaryKeyRelatedField(
        source='division_fiscale',
        queryset=DivisionFiscale.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )
    numero_tva_id = serializers.PrimaryKeyRelatedField(
        source='numero_tva',
        queryset=UserTVANumber.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Adresse
        fields = [
            "id",
            "utilisateur",
            "utilisation",
            "type_client",
            "nom_complet",
            "telephone",
            "raison_sociale",
            "numero_tva",        # objet lié complet en lecture
            "numero_tva_id",     # id en écriture
            "rccm",
            "ifu",
            "forme_juridique",   # objet lié complet en lecture
            "forme_juridique_id",# id en écriture
            "regime_fiscal",     # objet lié complet en lecture
            "regime_fiscal_id",  # id en écriture
            "division_fiscale",  # objet lié complet en lecture
            "division_fiscale_id",# id en écriture
            "rue",
            "numero",
            "ville",
            "code_postal",
            "pays",              # objet lié complet en lecture
            "pays_id",           # id en écriture
            "livraison_identique_facturation",
        ]
        read_only_fields = ["utilisateur"]

    def validate(self, attrs):
        """
        Validation simplifiée sans logique pays_afrique.
        Vérifie que pour un type_client 'entreprise', la raison sociale est présente.
        """
        instance = getattr(self, 'instance', None)

        type_client = attrs.get('type_client') or (instance.type_client if instance else None)
        raison_sociale = attrs.get('raison_sociale') or (getattr(instance, 'raison_sociale', None) if instance else None)

        if type_client == 'entreprise' and not raison_sociale:
            raise serializers.ValidationError({
                'raison_sociale': "Le champ 'raison_sociale' est obligatoire pour ce type d'entreprise."
            })

        return attrs'''
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import (
    Adresse,
    Role, Permission, RolePermission,
    UserTVANumber, HistoriqueConnexion , Pays, FormeJuridique, RegimeFiscal ,DivisionFiscale
)

User = get_user_model()


class UserTVANumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTVANumber
        fields = ['id', 'numero_tva', 'pays', 'date_ajout']

class PaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pays
        fields = ['id', 'nom', 'code_telephone']

class FormeJuridiqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormeJuridique
        fields = ['id', 'nom']

class RegimeFiscalSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegimeFiscal
        fields = ['id', 'nom']

class DivisionFiscaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DivisionFiscale
        fields = ['id', 'nom']

class AdresseSerializer(serializers.ModelSerializer):
    # Relations en lecture (détail complet)
    pays = PaysSerializer(read_only=True)
    forme_juridique = FormeJuridiqueSerializer(read_only=True)
    regime_fiscal = RegimeFiscalSerializer(read_only=True)
    division_fiscale = DivisionFiscaleSerializer(read_only=True)
    numero_tva = UserTVANumberSerializer(read_only=True)

    # Relations en écriture (via ID uniquement)
    pays_id = serializers.PrimaryKeyRelatedField(
        source='pays',
        queryset=Pays.objects.all(),
        write_only=True
    )
    forme_juridique_id = serializers.PrimaryKeyRelatedField(
        source='forme_juridique',
        queryset=FormeJuridique.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )
    regime_fiscal_id = serializers.PrimaryKeyRelatedField(
        source='regime_fiscal',
        queryset=RegimeFiscal.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )
    division_fiscale_id = serializers.PrimaryKeyRelatedField(
        source='division_fiscale',
        queryset=DivisionFiscale.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )
    numero_tva_id = serializers.PrimaryKeyRelatedField(
        source='numero_tva',
        queryset=UserTVANumber.objects.all(),
        write_only=True,
        allow_null=True,
        required=False
    )

    class Meta:
        model = Adresse
        fields = [
            "id",
            "utilisateur",
            "utilisation",
            "type_client",
            "nom_complet",
            "telephone",
            "raison_sociale",
            "numero_tva",        # objet lié complet en lecture
            "numero_tva_id",     # id en écriture
            "rccm",
            "ifu",
            "forme_juridique",   # objet lié complet en lecture
            "forme_juridique_id",# id en écriture
            "regime_fiscal",     # objet lié complet en lecture
            "regime_fiscal_id",  # id en écriture
            "division_fiscale",  # objet lié complet en lecture
            "division_fiscale_id",# id en écriture
            "rue",
            "numero",
            "ville",
            "code_postal",
            "pays",              # objet lié complet en lecture
            "pays_id",           # id en écriture
            "livraison_identique_facturation",
        ]
        read_only_fields = ["utilisateur"]

    def validate(self, attrs):
        """
        Validation simplifiée sans logique pays_afrique.
        Vérifie que pour un type_client 'entreprise', la raison sociale est présente.
        """
        instance = getattr(self, 'instance', None)

        type_client = attrs.get('type_client') or (instance.type_client if instance else None)
        raison_sociale = attrs.get('raison_sociale') or (getattr(instance, 'raison_sociale', None) if instance else None)

        if type_client == 'entreprise' and not raison_sociale:
            raise serializers.ValidationError({
                'raison_sociale': "Le champ 'raison_sociale' est obligatoire pour ce type d'entreprise."
            })

        return attrs

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']





class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'description']


class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission']


class HistoriqueConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueConnexion
        fields = ["id", "adresse_ip", "date_connexion", "user_agent"]

'''class UserSerializer(serializers.ModelSerializer):
    adresses = AdresseSerializer(many=True, required=False)
    user_roles = UserRoleSerializer(many=True, read_only=True)  # Affichage des rôles associés (lecture seule)
    numero_tva_valides = UserTVANumberSerializer(many=True, read_only=True)

    # Champ write-only roles acceptant une liste d’IDs de rôles à attribuer à la création ou maj
    roles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Role.objects.all(),
        write_only=True,
        required=False,
        help_text="Liste des IDs des rôles à attribuer"
    )

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        min_length=8,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'type_client', 'accepte_facture_electronique',
            'accepte_cgv', 'telephone', 'is_active', 'is_staff', 'date_joined', 'password',
            'adresses', 'user_roles', 'numero_tva_valides', 'roles'
        ]
        read_only_fields = ['is_active', 'is_staff', 'date_joined', 'user_roles', 'numero_tva_valides']

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        adresses_data = validated_data.pop('adresses', [])
        password = validated_data.pop('password', None)

        user = User(**validated_data)
        if not password:
            raise serializers.ValidationError({'password': 'Un mot de passe est requis.'})
        user.set_password(password)
        user.save()

        # Créer les adresses liées
        for addr_data in adresses_data:
            Adresse.objects.create(utilisateur=user, **addr_data)

        # Créer les rôles liés via UserRole
        for role in roles_data:
            UserRole.objects.create(user=user, role=role)

        return user

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', None)
        adresses_data = validated_data.pop('adresses', None)
        password = validated_data.pop('password', None)

        # Mise à jour champs simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # Mise à jour des adresses liées
        if adresses_data is not None:
            instance.adresses.all().delete()
            for addr_data in adresses_data:
                Adresse.objects.create(utilisateur=instance, **addr_data)

        # Mise à jour des rôles liés
        if roles_data is not None:
            UserRole.objects.filter(user=instance).delete()
            for role in roles_data:
                UserRole.objects.create(user=instance, role=role)

        return instance
'''

class UserSerializer(serializers.ModelSerializer):
    adresses = AdresseSerializer(many=True, required=False)
    roles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Role.objects.all(),
        write_only=True,
        required=False,
        help_text="Liste des IDs des rôles à attribuer"
    )
    roles_detail = RoleSerializer(many=True, read_only=True, source='roles')  # nested read

    numero_tva_valides = UserTVANumberSerializer(many=True, read_only=True)

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        min_length=8,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'type_client', 'accepte_facture_electronique',
            'accepte_cgv', 'telephone', 'is_active', 'is_staff', 'date_joined', 'password',
            'adresses', 'roles_detail', 'roles', 'numero_tva_valides'
        ]
        read_only_fields = ['is_active', 'is_staff', 'date_joined', 'roles_detail', 'numero_tva_valides']

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        adresses_data = validated_data.pop('adresses', [])
        password = validated_data.pop('password', None)

        user = User(**validated_data)
        if not password:
            raise serializers.ValidationError({'password': 'Un mot de passe est requis.'})
        user.set_password(password)
        user.save()

        # Create related addresses
        for addr_data in adresses_data:
            Adresse.objects.create(utilisateur=user, **addr_data)

        # Assign roles directly to the ManyToMany field
        user.roles.set(roles_data)

        return user

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', None)
        adresses_data = validated_data.pop('adresses', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # Update addresses
        if adresses_data is not None:
            instance.adresses.all().delete()
            for addr_data in adresses_data:
                Adresse.objects.create(utilisateur=instance, **addr_data)

        # Update roles
        if roles_data is not None:
            instance.roles.set(roles_data)

        return instance

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password], write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']




class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'description']


class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission']


class HistoriqueConnexionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoriqueConnexion
        fields = ["id", "adresse_ip", "date_connexion", "user_agent"]

class UserSerializer(serializers.ModelSerializer):
    adresses = AdresseSerializer(many=True, required=False)
    roles = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Role.objects.all(),
        write_only=True,
        required=False,
        help_text="Liste des IDs des rôles à attribuer"
    )
    roles_detail = RoleSerializer(many=True, read_only=True, source='roles')  # nested read

    numero_tva_valides = UserTVANumberSerializer(many=True, read_only=True)

    password = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=True,
        min_length=8,
        style={'input_type': 'password'},
    )

    class Meta:
        model = User
        fields = [
            'id', 'email', 'type_client', 'accepte_facture_electronique',
            'accepte_cgv', 'telephone', 'is_active', 'is_staff', 'date_joined', 'password',
            'adresses', 'roles_detail', 'roles', 'numero_tva_valides'
        ]
        read_only_fields = ['is_active', 'is_staff', 'date_joined', 'roles_detail', 'numero_tva_valides']

    def create(self, validated_data):
        roles_data = validated_data.pop('roles', [])
        adresses_data = validated_data.pop('adresses', [])
        password = validated_data.pop('password', None)

        user = User(**validated_data)
        if not password:
            raise serializers.ValidationError({'password': 'Un mot de passe est requis.'})
        user.set_password(password)
        user.save()

        # Create related addresses
        for addr_data in adresses_data:
            Adresse.objects.create(utilisateur=user, **addr_data)

        # Assign roles directly to the ManyToMany field
        user.roles.set(roles_data)

        return user

    def update(self, instance, validated_data):
        roles_data = validated_data.pop('roles', None)
        adresses_data = validated_data.pop('adresses', None)
        password = validated_data.pop('password', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()

        # Update addresses
        if adresses_data is not None:
            instance.adresses.all().delete()
            for addr_data in adresses_data:
                Adresse.objects.create(utilisateur=instance, **addr_data)

        # Update roles
        if roles_data is not None:
            instance.roles.set(roles_data)

        return instance


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True, write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password], write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
