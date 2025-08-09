from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from .views import UserViewSet ,RoleViewSet ,    AdresseViewSet, PaysViewSet, FormeJuridiqueViewSet, RegimeFiscalViewSet, DivisionFiscaleViewSet                                                                                                
router = DefaultRouter()

router.register(r'adresses', AdresseViewSet, basename='adresse')
router.register(r'roles' , RoleViewSet , basename='roles')
router.register(r'users', UserViewSet, basename='user')
router.register(r'usertvanumbers', UserTVANumberViewSet, basename='usertvanumber')
router.register(r'pays', PaysViewSet, basename='pays')
router.register(r'formejuridiques', FormeJuridiqueViewSet, basename='formejuridique')
router.register(r'regimefiscaux', RegimeFiscalViewSet, basename='regimefiscal')
router.register(r'divisionfiscales', DivisionFiscaleViewSet, basename='divisionfiscale')
urlpatterns = [  # IMPORTANT : attention                                                                                                                                                                     
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', LoginAPIView.as_view(), name='user-login'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path("users/<int:user_id>/historiques_connexion/", HistoriqueConnexionList.as_view(), name="user-historiques-connexion"),
    path('password/change/', ChangePasswordView.as_view(), name='password-change'),
    path('password/reset/request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('', include(router.urls)),
]
