from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.contrib.auth import get_user_model

User = get_user_model()

# Inscription d’un utilisateur
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer

class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'detail': 'Email et mot de passe requis.'}, status=status.HTTP_400_BAD_REQUEST)

        # Authentification via email comme username
        user = authenticate(request, username=email, password=password)

        if user is not None:
            if not user.is_active:
                return Response({'detail': 'Compte désactivé.'}, status=status.HTTP_403_FORBIDDEN)

            # Obtient ou crée un token TokenAuthentication
            token, created = Token.objects.get_or_create(user=user)

            serializer = UserSerializer(user)

            return Response({
                'token': token.key,
                'user': serializer.data
            }, status=status.HTTP_200_OK)

        return Response({'detail': 'Identifiants invalides.'}, status=status.HTTP_401_UNAUTHORIZED)

# Détail et mise à jour du profil utilisateur connecté uniquement
class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Gestion des rôles attribués aux utilisateurs (list, add, remove)
class UserRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        return UserRole.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Gestion des adresses
class AdresseViewSet(viewsets.ModelViewSet):
    serializer_class = AdresseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Adresse.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

# Gestion profils entreprise et particulier (création / mise à jour par utilisateur)
class ProfilEntrepriseViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilEntrepriseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProfilEntreprise.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

class ProfilParticulierViewSet(viewsets.ModelViewSet):
    serializer_class = ProfilParticulierSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return ProfilParticulier.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response({"old_password": ["Mot de passe actuel incorrect."]}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"detail": "Mot de passe modifié avec succès."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Ne pas révéler si l'email n'existe pas pour éviter fuite d'information
                return Response({"detail": "Un mail de réinitialisation a été envoyé si cet email est enregistré."})

            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = user.pk

            # Construire l'URL de réinitialisation à envoyer par email
            reset_url = request.build_absolute_uri(
                reverse('password-reset-confirm') + f"?uid={uid}&token={token}"
            )

            # Envoi email (adapter sujet et corps selon votre front / template)
            send_mail(
                subject="Réinitialisation de votre mot de passe",
                message=f"Pour réinitialiser votre mot de passe, veuillez cliquer sur ce lien : {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            return Response({"detail": "Un mail de réinitialisation a été envoyé."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.contrib.auth.tokens import PasswordResetTokenGenerator

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']

            try:
                user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                return Response({"detail": "Lien invalide."}, status=status.HTTP_400_BAD_REQUEST)

            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                return Response({"detail": "Token invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()
            return Response({"detail": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
