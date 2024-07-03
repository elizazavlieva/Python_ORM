# Generated by Django 5.0.4 on 2024-07-02 17:50

from django.db import migrations


class Migration(migrations.Migration):
    def create_unique_brands(apps, schema_editor):
        shoe = apps.get_model('main_app', 'Shoe')
        unique_brands = apps.get_model('main_app', 'UniqueBrands')

        unique_brand_names = shoe.objects.values_list('brand', flat=True).distinct()

        for brand_name in unique_brand_names:
            unique_brands.create(brand_name=brand_name)

    def reverse_unique_brands(apps, schema_editor):
        unique_brands = apps.get_model('main_app', 'UniqueBrands')
        unique_brands.objects.all().delete()

    dependencies = [
        ('main_app', '0002_uniquebrands'),
    ]

    operations = [
        migrations.RunPython(create_unique_brands, reverse_unique_brands)
    ]
