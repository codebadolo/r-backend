from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User,
    Role,
    UserRole,
    Permission,
    RolePermission,

    Adresse,
    UserTVANumber,
    HistoriqueConnexion,
)

admin.site.register(User)
admin.site.register(UserRole)
admin.site.register(UserTVANumber)
admin.site.register(Role)
  
admin.site.register(Adresse)