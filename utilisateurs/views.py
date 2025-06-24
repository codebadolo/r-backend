from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, permissions
from .models import User, Role, UserRole, Permission, RolePermission
from .serializers import UserSerializer, RoleSerializer, UserRoleSerializer, PermissionSerializer, RolePermissionSerializer

# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import LoginSerializer
from rest_framework.permissions import AllowAny
class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']

        # Création ou récupération du token
        token, created = Token.objects.get_or_create(user=user)

        # Renvoyer token et infos utilisateur (ex: rôles)
        roles = user.user_roles.values_list('role__name', flat=True)
        return Response({
            'token': token.key,
            'user': {
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'roles': list(roles),
            }
        })

# users/views.py
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    roles = user.user_roles.values_list('role__name', flat=True)
    data = {
        'email': user.email,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'roles': list(roles),
    }
    return Response(data)
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Supprime le token pour déconnecter l’utilisateur
        Token.objects.filter(user=request.user).delete()
        return Response({"detail": "Déconnexion réussie"}, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated]

class PermissionViewSet(viewsets.ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RolePermissionViewSet(viewsets.ModelViewSet):
    queryset = RolePermission.objects.all()
    serializer_class = RolePermissionSerializer
    permission_classes = [permissions.IsAuthenticated]
