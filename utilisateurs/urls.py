from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserViewSet
router = DefaultRouter()
router.register(r'user-roles', UserRoleViewSet, basename='userrole')  # <-- ici le basename
router.register(r'adresses', AdresseViewSet, basename='adresse')
router.register(r'users', UserViewSet, basename='user')
router.register(r'profils-entreprise', ProfilEntrepriseViewSet, basename='profilentreprise')
router.register(r'profils-particulier', ProfilParticulierViewSet, basename='profilparticulier')


urlpatterns = [  # IMPORTANT : attention                                                                                                                                                                     
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
     
        path('password/change/', ChangePasswordView.as_view(), name='password-change'),
    path('password/reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('', include(router.urls)),
]
