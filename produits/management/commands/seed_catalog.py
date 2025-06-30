from django.core.management.base import BaseCommand
from produits.models import Brand, Category, ProductType, ProductAttribute, ProductTypeAttribute

class Command(BaseCommand):
    help = "Seed catalog with brands, categories, product types, and attributes (no products or inventory)."

    def handle(self, *args, **kwargs):
        # 1. Brands
        brands = [
            "Dell", "HP", "Lenovo", "Cisco", "Microsoft", "Apple", "Asus", "Synology", "Fortinet"
        ]
        for name in brands:
            Brand.objects.get_or_create(name=name)
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(brands)} brands."))

        # 2. Categories & Subcategories
        categories = {
            "Computers": ["Laptops", "Desktops", "Workstations", "All-in-One PCs"],
            "Networking": ["Routers", "Switches", "Firewalls", "Access Points"],
            "Systems": ["Servers", "Storage", "NAS", "UPS"],
            "Software": ["Operating Systems", "Productivity", "Security", "Virtualization"]
        }
        for parent_name, subcats in categories.items():
            parent, _ = Category.objects.get_or_create(name=parent_name, parent=None)
            for sub in subcats:
                Category.objects.get_or_create(name=sub, parent=parent)
        self.stdout.write(self.style.SUCCESS("Seeded categories and subcategories."))

        # 3. Product Types
        product_types = [
            "Laptop", "Desktop", "Server", "Router", "Switch", "Firewall", "NAS", "UPS", "Operating System", "Office Suite", "Antivirus", "Virtualization Platform"
        ]
        pt_objs = {}
        for pt in product_types:
            obj, _ = ProductType.objects.get_or_create(name=pt)
            pt_objs[pt] = obj
        self.stdout.write(self.style.SUCCESS(f"Seeded {len(product_types)} product types."))

        # 4. Attributes (and link to types)
        attributes = {
            # attribute: [description, [product_types]]
            "Processor": ["CPU model/type", ["Laptop", "Desktop", "Server"]],
            "RAM": ["Memory size", ["Laptop", "Desktop", "Server"]],
            "Storage": ["Disk/SSD capacity", ["Laptop", "Desktop", "Server", "NAS"]],
            "Operating System": ["OS version", ["Laptop", "Desktop", "Server", "Operating System"]],
            "Ports": ["Available ports", ["Laptop", "Desktop", "Server", "Router", "Switch", "Firewall"]],
            "Power": ["Power rating", ["UPS"]],
            "License": ["License type", ["Operating System", "Office Suite", "Antivirus", "Virtualization Platform"]],
            "Throughput": ["Max throughput", ["Router", "Switch", "Firewall"]],
            "Vendor": ["Vendor name", ["NAS", "UPS", "Firewall", "Router", "Switch"]],
        }
        for attr_name, (desc, pt_list) in attributes.items():
            attr_obj, _ = ProductAttribute.objects.get_or_create(name=attr_name, defaults={"description": desc})
            for pt_name in pt_list:
                pt_obj = pt_objs.get(pt_name)
                if pt_obj:
                    ProductTypeAttribute.objects.get_or_create(product_type=pt_obj, product_attribute=attr_obj)
        self.stdout.write(self.style.SUCCESS("Seeded attributes and linked them to product types."))

        self.stdout.write(self.style.SUCCESS("Catalog seeding complete!"))
