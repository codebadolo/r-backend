from django.core.management.base import BaseCommand
from django.db.models import Count
from produits.models import (
    Category, Brand, ProductType,
    ProductAttribute, ProductAttributeOption,
    ProductAttributeValue, Warehouse
)

class Command(BaseCommand):
    help = "Detect and remove duplicate objects in key models."

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting duplicate cleanup...")

        # Define models and unique fields combos to check for duplicates
        # key: model, value: tuple of fields that should be unique
        models_to_clean = {
            Category: ('name', 'parent'),
            Brand: ('name',),
            ProductType: ('name',),
            ProductAttribute: ('name', 'product_type'),
            ProductAttributeOption: ('attribute', 'value'),
            ProductAttributeValue: ('product', 'option'),
            Warehouse: ('name', 'location'),
        }

        total_deleted = 0

        for model, unique_fields in models_to_clean.items():
            self.stdout.write(f"Processing model {model.__name__} for duplicates by fields {unique_fields}")

            # Find duplicates: group by unique fields having count > 1
            duplicates = (
                model.objects
                .values(*unique_fields)
                .annotate(dupe_count=Count('id'))
                .filter(dupe_count__gt=1)
            )

            model_deleted = 0
            for dup in duplicates:
                filter_kwargs = {field: dup[field] for field in unique_fields}
                queryset = model.objects.filter(**filter_kwargs).order_by('id')

                # Keep one, delete others (all except first)
                ids_to_delete = list(queryset.values_list('id', flat=True)[1:])
                if ids_to_delete:
                    deleted, _ = model.objects.filter(id__in=ids_to_delete).delete()
                    model_deleted += deleted

            self.stdout.write(f"Deleted {model_deleted} duplicate entries from {model.__name__}")
            total_deleted += model_deleted

        self.stdout.write(self.style.SUCCESS(f"Duplicate cleanup completed. Total deleted: {total_deleted}"))
