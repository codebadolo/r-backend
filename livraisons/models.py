from django.db import models
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class AdresseLivraison(models.Model):
    """
    Adresse où l'on livre les commandes.
    """
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name='adresses_livraison')
    nom_complet = models.CharField(max_length=255)
    adresse_ligne1 = models.CharField(max_length=255)
    adresse_ligne2 = models.CharField(max_length=255, blank=True, null=True)
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=20)
    pays = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    instructions_livraison = models.TextField(blank=True, null=True)  # ex : "sonner à l'interphone"

    def __str__(self):
        return f"{self.nom_complet} - {self.adresse_ligne1}, {self.ville}"


class Transporteur(models.Model):
    """
    Entreprise ou service de livraison.
    """
    nom = models.CharField(max_length=255)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    site_web = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom


class ModeLivraison(models.Model):
    """
    Différentes options de livraison proposées (ex : standard, express).
    """
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    delai_estime = models.CharField(max_length=100, blank=True, null=True)  # ex : "2-4 jours ouvrés"
    frais = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)
    transporteur = models.ForeignKey(Transporteur, on_delete=models.PROTECT, related_name='modes_livraison')
    actif = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} ({self.transporteur.nom})"


class Expedition(models.Model):
    """
    Instance d’une expédition liée à une commande.
    """
    commande = models.OneToOneField('commandes.Commande', on_delete=models.CASCADE, related_name='expedition')
    mode_livraison = models.ForeignKey(ModeLivraison, on_delete=models.PROTECT)
    adresse_livraison = models.ForeignKey(AdresseLivraison, on_delete=models.PROTECT)
    numero_suivi = models.CharField(max_length=100, blank=True, null=True)
    date_expedition = models.DateTimeField(blank=True, null=True)
    date_livraison_prevue = models.DateTimeField(blank=True, null=True)
    date_livraison_effective = models.DateTimeField(blank=True, null=True)
    statut_choices = [
        ('en_preparation', 'En préparation'),
        ('expediee', 'Expédiée'),
        ('en_transport', 'En transport'),
        ('livree', 'Livrée'),
        ('retour', 'Retour'),
        ('annulee', 'Annulée'),
    ]
    statut = models.CharField(max_length=20, choices=statut_choices, default='en_preparation')
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Expédition commande #{self.commande.id} - {self.get_statut_display()}"


class CentreLogistique(models.Model):
    """
    Centres ou entrepôts de préparation et gestion logistique.
    """
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    actif = models.BooleanField(default=True)

    def __str__(self):
        return self.nom


class PreparationCommande(models.Model):
    """
    Suivi de la préparation d’une commande dans un centre logistique.
    """
    commande = models.OneToOneField('commandes.Commande', on_delete=models.CASCADE, related_name='preparation')
    centre_logistique = models.ForeignKey(CentreLogistique, on_delete=models.PROTECT)
    date_debut_preparation = models.DateTimeField(blank=True, null=True)
    date_fin_preparation = models.DateTimeField(blank=True, null=True)
    statut_choices = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('prete', 'Prête à expédier'),
        ('annulee', 'Annulée'),
    ]
    statut = models.CharField(max_length=20, choices=statut_choices, default='en_attente')
    commentaire = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Préparation commande #{self.commande.id} - {self.get_statut_display()}"
