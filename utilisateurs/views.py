from rest_framework import viewsets, generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings

from .serializers import *
from .models import UserTVANumber, UserRole, Adresse

User = get_user_model()


# Inscription d’un utilisateur
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


# CRUD complet sur les utilisateurs (accessible uniquement aux utilisateurs authentifiés)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    # Si besoin, restreindre la visibilité selon droits ou utilisateur connecté

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [permissions.IsAuthenticated]  # ou AllowAny selon 
# Authentification via email + mot de passe avec TokenAuth DRF
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

# Récupération et mise à jour du profil utilisateur connecté uniquement ("Mon profil")
class UserDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Gestion des rôles utilisateurs (CRUD complet) - réservé aux admins
class UserRoleViewSet(viewsets.ModelViewSet):
    serializer_class = UserRoleSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

    def get_queryset(self):
        return UserRole.objects.all()

    def perform_create(self, serializer):
        # Optionnel : vous pouvez modifier qui est assigné selon votre logique
        serializer.save(user=self.request.user)


class AdresseViewSet(viewsets.ModelViewSet):
    queryset = Adresse.objects.all()
    serializer_class = AdresseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Par exemple, filtrer par utilisateur connecté
        user = self.request.user
        return Adresse.objects.filter(utilisateur=user)

    def perform_create(self, serializer):
        # Assigne automatiquement l’utilisateur connecté
        serializer.save(utilisateur=self.request.user)


class PaysViewSet(viewsets.ModelViewSet):
    queryset = Pays.objects.all()
    serializer_class = PaysSerializer
    permission_classes = [permissions.AllowAny]  # Liste ouverte


class FormeJuridiqueViewSet(viewsets.ModelViewSet):
    queryset = FormeJuridique.objects.all()
    serializer_class = FormeJuridiqueSerializer
    permission_classes = [permissions.AllowAny]


class RegimeFiscalViewSet(viewsets.ModelViewSet):
    queryset = RegimeFiscal.objects.all()
    serializer_class = RegimeFiscalSerializer
    permission_classes = [permissions.AllowAny]


class DivisionFiscaleViewSet(viewsets.ModelViewSet):
    queryset = DivisionFiscale.objects.all()
    serializer_class = DivisionFiscaleSerializer
    permission_classes = [permissions.AllowAny]


# Changement de mot de passe utilisateur authentifié
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response(
                    {"old_password": ["Mot de passe actuel incorrect."]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                {"detail": "Mot de passe modifié avec succès."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Demande de réinitialisation du mot de passe (envoi d'email)
class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                # Réponse identique pour éviter fuite d'info
                return Response(
                    {
                        "detail": "Un mail de réinitialisation a été envoyé si cet email est enregistré."
                    }
                )

            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            uid = user.pk

            reset_url = request.build_absolute_uri(
                reverse("password-reset-confirm") + f"?uid={uid}&token={token}"
            )

            send_mail(
                subject="Réinitialisation de votre mot de passe",
                message=f"Pour réinitialiser votre mot de passe, cliquez sur ce lien : {reset_url}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
            return Response(
                {"detail": "Un mail de réinitialisation a été envoyé."},
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Confirmation de réinitialisation du mot de passe avec uid et token
class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            uid = serializer.validated_data["uid"]
            token = serializer.validated_data["token"]
            new_password = serializer.validated_data["new_password"]

            try:
                user = User.objects.get(pk=uid)
            except User.DoesNotExist:
                return Response({"detail": "Lien invalide."}, status=status.HTTP_400_BAD_REQUEST)

            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, token):
                return Response(
                    {"detail": "Token invalide ou expiré."}, status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(new_password)
            user.save()
            return Response(
                {"detail": "Mot de passe réinitialisé avec succès."}, status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CRUD sur UserTVANumber, filtrage optionnel par utilisateur et création user liée automatiquement
class UserTVANumberViewSet(viewsets.ModelViewSet):
    serializer_class = UserTVANumberSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        utilisateur_id = self.request.query_params.get("utilisateur")
        if utilisateur_id:
            return UserTVANumber.objects.filter(utilisateur__id=utilisateur_id)
        # Par défaut, ne donner que les numéros TVA de l'utilisateur connecté
        return UserTVANumber.objects.filter(utilisateur=self.request.user)

    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)
