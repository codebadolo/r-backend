from django.db import models

# Create your models here.
from django.db import models

class Newsletter(models.Model):
    sujet = models.CharField(max_length=255)
    contenu = models.TextField()
    date_envoi = models.DateTimeField()
    actif = models.BooleanField(default=True)
    audience_segment = models.CharField(max_length=255, blank=True, null=True)  # Pour ciblage optionnel

    def __str__(self):
        return self.sujet


class InscriptionNewsletter(models.Model):
    email = models.EmailField(unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)
    actif = models.BooleanField(default=True)
    desinscription_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email


class CampagneMarketing(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    audience_segment = models.CharField(max_length=255, blank=True, null=True)  # Ciblage de la campagne
    termine = models.BooleanField(default=False)

    def __str__(self):
        return self.titre


class BannièreMarketing(models.Model):
    image_url = models.URLField()
    lien = models.URLField(blank=True, null=True)
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    actif = models.BooleanField(default=True)
    zone_affichage = models.CharField(max_length=255, blank=True, null=True)  # ex : 'homepage', 'fiche_produit'

    def __str__(self):
        return f"Bannière pour {self.zone_affichage}"


class TrackingOuverture(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    email = models.EmailField()
    date_ouverture = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Ouverture par {self.email} le {self.date_ouverture}"


class TrackingClic(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    email = models.EmailField()
    lien_clic = models.URLField()
    date_clic = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Clic par {self.email} sur {self.lien_clic}"
