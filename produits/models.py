from django.db import models
from storer import settings
class Category(models.Model):
    nom = models.CharField(max_length=255)
    parent_category = models.ForeignKey(
        'self', null=True, blank=True, on_delete=models.CASCADE, related_name='subcategories'
    )
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


class Brand(models.Model):
    nom = models.CharField(max_length=255)
    logo_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    etat = models.CharField(max_length=50, default='disponible')
    image_url = models.URLField(blank=True, null=True)
    ean_code = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nom


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    nom = models.CharField(max_length=255)  # ex: "16 Go RAM"
    valeur = models.CharField(max_length=255)  # ex: "Oui", "Noir", "512 Go"
    prix_supplémentaire = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    stock = models.IntegerField(default=0)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.product.nom} - {self.nom}: {self.valeur}"


class SpecCategory(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nom


class SpecKey(models.Model):
    DATA_TYPE_CHOICES = [
        ('string', 'Texte'),
        ('int', 'Nombre entier'),
        ('bool', 'Booléen'),
        ('list', 'Liste'),
        ('float', 'Nombre décimal'),
    ]

    spec_category = models.ForeignKey(SpecCategory, on_delete=models.CASCADE, related_name='spec_keys')
    nom_attribut = models.CharField(max_length=255)
    data_type = models.CharField(max_length=10, choices=DATA_TYPE_CHOICES, default='string')
    unit = models.CharField(max_length=20, blank=True, null=True)
    is_filterable = models.BooleanField(default=False)
    position = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.nom_attribut} ({self.spec_category.nom})"


class ProductSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    spec_key = models.ForeignKey(SpecKey, on_delete=models.CASCADE, related_name='product_specifications')
    valeur = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product.nom} - {self.spec_key.nom_attribut}: {self.valeur}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image de {self.product.nom}"


class ProductDocument(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='documents')
    url_document = models.URLField()
    type_document = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Document ({self.type_document}) pour {self.product.nom}"


class RelatedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_from')
    related_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='related_to')
    relation_type = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.product.nom} lié à {self.related_product.nom} ({self.relation_type})"


class Warehouse(models.Model):
    nom = models.CharField(max_length=255)
    adresse = models.CharField(max_length=255)
    code_postal = models.CharField(max_length=20)
    ville = models.CharField(max_length=100)
    pays = models.CharField(max_length=100)
    type = models.CharField(max_length=50, default='physique')
    is_active = models.BooleanField(default=True)
    commentaire = models.TextField(blank=True, null=True)

class StockLevel(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_levels')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.CASCADE)
    stock_total = models.IntegerField(default=0)
    stock_reserve = models.IntegerField(default=0)
    seuil_alerte = models.IntegerField(default=0)

class StockMovement(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stock_movements')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, null=True, blank=True, on_delete=models.CASCADE)
    mouvement_type = models.CharField(max_length=20)
    quantite = models.IntegerField()
    date_mouvement = models.DateTimeField(auto_now_add=True)
    commentaire = models.TextField(blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL)
