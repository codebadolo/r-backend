from django.db import models
from django.utils.text import slugify

# 1. Marque (Brand)
class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True)
    logo = models.ImageField(upload_to='brands/logos/', blank=True, null=True)

    def __str__(self):
        return self.name

# 2. Catégorie (Category)
class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.SET_NULL)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# 4. Type de Produit (ProductType)
class ProductType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

# 5. Attribut de Produit (ProductAttribute)
class ProductAttribute(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# 6. Valeur d’Attribut de Produit (ProductAttributeValue)
class ProductAttributeValue(models.Model):
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='values')
    value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.product_attribute.name}: {self.value}"

# 7. Liaison TypeProduit ↔ Attribut (ProductTypeAttribute)
class ProductTypeAttribute(models.Model):
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='type_attributes')
    product_attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, related_name='attribute_types')

    class Meta:
        unique_together = ('product_type', 'product_attribute')

    def __str__(self):
        return f"{self.product_type.name} - {self.product_attribute.name}"

# 3. Produit (Product)
class Product(models.Model):
    web_id = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='products')
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='products')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# 8. Variante de Produit (ProductInventory)
class ProductInventory(models.Model):
    sku = models.CharField(max_length=100, unique=True)
    upc = models.CharField(max_length=12, blank=True, null=True)
    product_type = models.ForeignKey(ProductType, on_delete=models.PROTECT, related_name='inventories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name='inventories')
    attributes = models.ManyToManyField(ProductAttributeValue, related_name='inventories', blank=True)
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    retail_price = models.DecimalField(max_digits=10, decimal_places=2)
    store_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_digital = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=8, decimal_places=3, null=True, blank=True)  # poids en kg
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} - {self.sku}"

# 9. Association ValeurAttribut ↔ Variante (ProductAttributeValues)
class ProductAttributeValues(models.Model):
    product_attribute_value = models.ForeignKey(ProductAttributeValue, on_delete=models.CASCADE, related_name='attribute_values')
    product_inventory = models.ForeignKey(ProductInventory, on_delete=models.CASCADE, related_name='attribute_values')

    class Meta:
        unique_together = ('product_attribute_value', 'product_inventory')

    def __str__(self):
        return f"{self.product_inventory.sku} - {self.product_attribute_value}"

# 10. Média (Media)
class Media(models.Model):
    product_inventory = models.ForeignKey(ProductInventory, on_delete=models.CASCADE, related_name='media')
    img_url = models.ImageField(upload_to='products/media/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Media for {self.product_inventory.sku}"

# 11. Stock (Stock)
class Stock(models.Model):
    product_inventory = models.OneToOneField(ProductInventory, on_delete=models.CASCADE, related_name='stock')
    last_checked = models.DateTimeField(auto_now=True)
    units = models.PositiveIntegerField(default=0)
    units_sold = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Stock for {self.product_inventory.sku}: {self.units} units"

# 12. Section de Spécification (SectionSpecification)
class SectionSpecification(models.Model):
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

# 13. Clé de Spécification (CleSpecification)
class CleSpecification(models.Model):
    name = models.CharField(max_length=255)
    section = models.ForeignKey(SectionSpecification, on_delete=models.CASCADE, related_name='keys')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

# 14. Spécification Produit (ProduitSpecification)
class ProduitSpecification(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='specifications')
    cle_specification = models.ForeignKey(CleSpecification, on_delete=models.CASCADE, related_name='product_specs')
    value = models.TextField()

    class Meta:
        unique_together = ('product', 'cle_specification')

    def __str__(self):
        return f"{self.product.name} - {self.cle_specification.name}: {self.value}"
