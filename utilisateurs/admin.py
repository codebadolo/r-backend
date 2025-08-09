from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User, Role, Permission, RolePermission,
    UserTVANumber, HistoriqueConnexion,
    Adresse, Pays, FormeJuridique, RegimeFiscal, DivisionFiscale
)
from .models import (
    UserTVANumber, Pays, FormeJuridique, RegimeFiscal, DivisionFiscale
)



# --- Inline for Addresses ---
class AdresseInline(admin.TabularInline):
    model = Adresse
    extra = 0  # No extra blank forms
    fields = (
        'utilisation', 'type_client', 'nom_complet', 'telephone', 'raison_sociale',
        'numero_tva', 'pays', 'forme_juridique', 'regime_fiscal', 'division_fiscale',
        'rccm', 'ifu', 'rue', 'numero', 'ville', 'code_postal', 'livraison_identique_facturation'
    )
    readonly_fields = ()
    #autocomplete_fields = ('numero_tva', 'pays', 'forme_juridique', 'regime_fiscal', 'division_fiscale')


# --- Custom UserAdmin ---
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    # Fields to be used in displaying the User model.
    # We override to use email as username.
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {
            'fields': (
                'type_client', 'telephone',
                'accepte_facture_electronique', 'accepte_cgv',
            )
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'roles', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'type_client', 'roles'),
        }),
    )
    list_display = ('email', 'type_client' , 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'roles')
    search_fields = ('email', 'telephone')
    ordering = ('email',)
    filter_horizontal = ('roles', 'groups', 'user_permissions')
    inlines = [AdresseInline]

# --- Register Role with list display ---
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

# --- Permission Admin ---
@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    list_display = ('code', 'description')
    search_fields = ('code',)

# --- RolePermission Admin ---
@admin.register(RolePermission)
class RolePermissionAdmin(admin.ModelAdmin):
    list_display = ('role', 'permission')
    list_filter = ('role', 'permission')

# --- UserTVANumber Admin ---
@admin.register(UserTVANumber)
class UserTVANumberAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'numero_tva', 'pays', 'date_ajout')
    search_fields = ('numero_tva', 'pays__nom', 'utilisateur__email')

# --- HistoriqueConnexion Admin ---
@admin.register(HistoriqueConnexion)
class HistoriqueConnexionAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'date_connexion', 'adresse_ip')
    list_filter = ('date_connexion',)
    search_fields = ('utilisateur__email', 'adresse_ip')

# --- Register reference tables ---
admin.site.register(Pays)
admin.site.register(FormeJuridique)
admin.site.register(RegimeFiscal)
admin.site.register(DivisionFiscale)
admin.site.register(Adresse)  # Also register standalone if needed


# Optional: Customizing admin site headers and titles
admin.site.site_header = "ROH Store Administration"
admin.site.site_title = "ROH Store Admin Portal"
admin.site.index_title = "Welcome to ROH Store Admin"
