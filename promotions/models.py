from django.db import models
from django.contrib.auth import get_user_model
from commandes.models import Commande
from produits.models import Product,Category
Utilisateur = get_user_model()

class Promotion(models.Model):
    """
    Promotion globale pouvant représenter plusieurs types d'offres.
    """
    TYPE_CHOIX = [
        ('pourcentage', 'Pourcentage'),
        ('montant', 'Montant fixe'),
        ('produit_offert', 'Produit offert'),
        ('livraison_gratuite', 'Livraison gratuite'),
    ]

    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    type_promo = models.CharField(max_length=20, choices=TYPE_CHOIX)
    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)  # Pour promotions liées à un coupon
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    quantite_max = models.PositiveIntegerField(null=True, blank=True)  # Limite d’utilisation globale
    utilisations = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    limite_par_utilisateur = models.PositiveIntegerField(null=True, blank=True)  # Limite d’utilisation par utilisateur

    def est_valide(self):
        """
        Vérifie si la promotion est active, dans la période et sous la limite d'utilisation.
        """
        from django.utils import timezone
        maintenant = timezone.now()
        if not self.actif:
            return False
        if self.date_debut > maintenant or self.date_fin < maintenant:
            return False
        if self.quantite_max is not None and self.utilisations >= self.quantite_max:
            return False
        return True

    def __str__(self):
        return f"{self.nom} ({self.code if self.code else 'sans code'})"


class ConditionPromotion(models.Model):
    """
    Condition d’éligibilité à une promotion spécifique.
    """
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='conditions')
    produit = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    categorie = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE)
    montant_min_panier = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    utilisateur = models.ForeignKey(Utilisateur, null=True, blank=True, on_delete=models.CASCADE)
    nb_utilisations_par_utilisateur = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        conditions = []
        if self.produit:
            conditions.append(f"Produit : {self.produit.nom}")
        if self.categorie:
            conditions.append(f"Catégorie : {self.categorie.nom}")
        if self.montant_min_panier:
            conditions.append(f"Panier mini : {self.montant_min_panier}€")
        if self.utilisateur:
            conditions.append(f"Utilisateur : {self.utilisateur.username}")
        return f"Conditions pour {self.promotion.nom} — " + ", ".join(conditions) if conditions else f"Conditions pour {self.promotion.nom}"


class ApplicationPromotion(models.Model):
    """
    Enregistrement de l'utilisation d'une promotion sur une commande.
    """
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='applications')
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='promotions_appliquees')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    montant_remise = models.DecimalField(max_digits=10, decimal_places=2)
    date_application = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Promo '{self.promotion.nom}' appliquée sur commande #{self.commande.id}"


class Coupon(models.Model):
    """
    Coupon spécifique avec code distinct et gestion d’utilisation.
    """
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)
    TYPE_REMISE_CHOIX = [
        ('pourcentage', 'Pourcentage'),
        ('montant', 'Montant fixe'),
        ('livraison_gratuite', 'Livraison gratuite'),
    ]
    type_remise = models.CharField(max_length=20, choices=TYPE_REMISE_CHOIX, default='montant')
    valeur = models.DecimalField(max_digits=10, decimal_places=2)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    quantite_max = models.PositiveIntegerField(null=True, blank=True)
    utilisations = models.PositiveIntegerField(default=0)
    actif = models.BooleanField(default=True)
    limite_par_utilisateur = models.PositiveIntegerField(null=True, blank=True)

    def est_valide(self):
        from django.utils import timezone
        now = timezone.now()
        if not self.actif or self.date_debut > now or self.date_fin < now:
            return False
        if self.quantite_max is not None and self.utilisations >= self.quantite_max:
            return False
        return True

    def __str__(self):
        return self.code


class UsageCoupon(models.Model):
    """
    Historique d’utilisation d’un coupon par utilisateur pour une commande.
    """
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name='usages')
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE)
    date_utilisation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Coupon {self.coupon.code} utilisé par {self.utilisateur.username} sur commande #{self.commande.id}"
