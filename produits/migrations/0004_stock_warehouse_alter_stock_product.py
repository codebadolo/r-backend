# Generated by Django 5.2.3 on 2025-07-18 18:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produits', '0003_alter_productimage_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='warehouse',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='produits.warehouse'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='produits.product'),
        ),
    ]
