from django.db import models
from django.contrib.auth import get_user_model
from produits.models import Product , ProductVariant
Utilisateur = get_user_model()

class Adresse(models.Model):
    """
    Adresse de facturation ou de livraison liée à un utilisateur
    """
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='adresses')
    nom_complet = models.CharField(max_length=255)
    adresse_ligne1 = models.CharField(max_length=255)
    adresse_ligne2 = models.CharField(max_length=255, blank=True)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
    pays = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True)
    est_facturation = models.BooleanField(default=False)
    est_livraison = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom_complet} - {self.adresse_ligne1}, {self.ville}"


class Panier(models.Model):
    """
    Panier associé à un utilisateur, stock temporaire avant commande
    """
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name='panier')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def prix_total(self):
        return sum(item.prix_total() for item in self.elements.all())

    def __str__(self):
        return f"Panier de {self.utilisateur.username}"


class ElementPanier(models.Model):
    """
    Ligne du panier : produit + variante + quantité
    """
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE, related_name='elements')
    produit = models.ForeignKey(Product, on_delete=models.PROTECT)
    variante = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(default=1)

    def prix_unitaire(self):
        if self.variante:
            prix_base = self.produit.prix + self.variante.prix_supplémentaire
        else:
            prix_base = self.produit.prix
        return prix_base

    def prix_total(self):
        return self.prix_unitaire() * self.quantite

    def __str__(self):
        return f"{self.quantite} x {self.produit.nom}"


class Commande(models.Model):
    """
    Commande validée par un client
    """
    STATUTS = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours de traitement'),
        ('expediee', 'Expédiée'),
        ('livree', 'Livrée'),
        ('annulee', 'Annulée'),
    ]

    MODES_PAIEMENT = [
        ('stripe', 'Stripe'),
        ('paypal', 'Paypal'),
        ('paiement_livraison', 'Paiement à la livraison'),
        # ajouter d’autres modes
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='commandes')
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(max_length=20, choices=STATUTS, default='en_attente')
    mode_paiement = models.CharField(max_length=30, choices=MODES_PAIEMENT)
    paiement_valide = models.BooleanField(default=False)
    adresse_livraison = models.ForeignKey(Adresse, related_name='livraisons', on_delete=models.PROTECT)
    adresse_facturation = models.ForeignKey(Adresse, related_name='facturations', on_delete=models.PROTECT)
    telephone = models.CharField(max_length=20)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Commande #{self.id} - {self.utilisateur.username}"

    def mettre_a_jour_prix_total(self):
        total = sum(item.prix_total for item in self.elements.all())
        self.prix_total = total
        self.save()


class ElementCommande(models.Model):
    """
    Ligne détaillée d’une commande : produit, variante et quantités
    """
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='elements')
    produit = models.ForeignKey(Product, on_delete=models.PROTECT)
    variante = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.PROTECT)
    quantite = models.PositiveIntegerField(default=1)
    prix_unitaire = models.DecimalField(max_digits=10, decimal_places=2)
    prix_total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.produit.nom} (x{self.quantite})"

    def save(self, *args, **kwargs):
        self.prix_total = self.prix_unitaire * self.quantite
        super().save(*args, **kwargs)
        self.commande.mettre_a_jour_prix_total()


class Paiement(models.Model):
    """
    Données de paiement liées à une commande
    """
    commande = models.OneToOneField(Commande, on_delete=models.CASCADE, related_name='paiement')
    identifiant_transaction = models.CharField(max_length=255, blank=True, null=True)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=50)
    statut = models.CharField(max_length=50)  # success, failed, pending, etc.
    details = models.JSONField(blank=True, null=True)

    def __str__(self):
        return f"Paiement {self.id} - {self.statut} - {self.montant}€"


class HistoriqueStatutCommande(models.Model):
    """
    Historique des changements de statut pour audit / notifications
    """
    commande = models.ForeignKey(Commande, on_delete=models.CASCADE, related_name='historique_statuts')
    ancien_statut = models.CharField(max_length=20)
    nouveau_statut = models.CharField(max_length=20)
    date_modification = models.DateTimeField(auto_now_add=True)
    modifie_par = models.ForeignKey(Utilisateur, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"Commande #{self.commande.id} : {self.ancien_statut} → {self.nouveau_statut} le {self.date_modification}"
