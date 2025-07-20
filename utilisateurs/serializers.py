from rest_framework import serializers
from .models import User, Role, UserRole, Permission, RolePermission

# users/serializers.py
from django.contrib.auth import authenticate
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user and user.is_active:
            data['user'] = user
            return data
        raise serializers.ValidationError("Email ou mot de passe incorrect")

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description']
class UserSerializer(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'date_joined', 'roles']

    def get_roles(self, obj):
        return RoleSerializer([ur.role for ur in obj.user_roles.all()], many=True).data



class UserRoleSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    role = RoleSerializer(read_only=True)  # décommenté ici
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='user', write_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)  # Ajoutez role_id

    class Meta:
        model = UserRole
        fields = ['id', 'user', 'role', 'assigned_at', 'user_id', 'role_id']


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'code', 'description']

class RolePermissionSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    permission = PermissionSerializer(read_only=True)
    role_id = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all(), source='role', write_only=True)
    permission_id = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), source='permission', write_only=True)

    class Meta:
        model = RolePermission
        fields = ['id', 'role', 'permission', 'role_id', 'permission_id']
