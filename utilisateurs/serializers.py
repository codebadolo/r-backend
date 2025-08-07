from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    ProfilEntreprise, ProfilParticulier, Adresse,
    Role, UserRole, Permission, RolePermission,
    UserTVANumber, HistoriqueConnexion
)

User = get_user_model()

class UserTVANumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTVANumber
        fields = ['id', 'numero_tva', 'pays', 'date_ajout']

class AdresseSerializer(serializers.ModelSerializer):
    numero_tva = UserTVANumberSerializer(read_only=True)
    numero_tva_id = serializers.PrimaryKeyRelatedField(queryset=UserTVANumber.objects.all(), source='numero_tva', write_only=True, allow_null=True, required=False)

    class Meta:
        model = Adresse
        fields = [
            'id', 'utilisateur', 'utilisation', 'nom_complet', 'telephone', 'raison_sociale', 'numero_siret',
            'numero_tva', 'numero_tva_id',
            'rue', 'numero', 'complement', 'ville', 'code_postal', 'pays'
        ]
        read_only_fields = ['utilisateur']

class ProfilEntrepriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilEntreprise
        fields = [
            'id', 'utilisateur', 'raison_sociale', 'numero_siret',
            'numero_tva', 'adresse_societe', 'telephone_suppl'
        ]
        read_only_fields = ['utilisateur']

class ProfilParticulierSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilParticulier
        fields = ['id', 'utilisateur', 'date_naissance']
        read_only_fields = ['utilisateur']

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']

class UserRoleSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    
    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'role_id', 'assigned_at']
        read_only_fields = ['user', 'assigned_at']

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
        fields = ['id', 'utilisateur', 'adresse_ip', 'date_connexion', 'user_agent']
        read_only_fields = ['utilisateur', 'date_connexion']

class UserSerializer(serializers.ModelSerializer):
    profils_entreprise = ProfilEntrepriseSerializer(source='profil_entreprise', read_only=True)
    profils_particulier = ProfilParticulierSerializer(source='profil_particulier', read_only=True)
    adresses = AdresseSerializer(many=True, read_only=True)
    user_roles = UserRoleSerializer(many=True, read_only=True)
    numero_tva_valides = UserTVANumberSerializer(many=True, read_only=True)

    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'type_client', 'accepte_facture_electronique',
            'accepte_cgv', 'telephone', 'is_active', 'is_staff', 'date_joined', 'password',
            'profils_entreprise', 'profils_particulier', 'adresses', 'user_roles', 'numero_tva_valides'
        ]
        read_only_fields = ['is_active', 'is_staff', 'date_joined']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

from rest_framework import serializers
from django.contrib.auth import password_validation

from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.IntegerField()
    token = serializers.CharField()
    new_password = serializers.CharField(validators=[validate_password])
    confirm_password = serializers.CharField()

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError("Les mots de passe ne correspondent pas.")
        return attrs
