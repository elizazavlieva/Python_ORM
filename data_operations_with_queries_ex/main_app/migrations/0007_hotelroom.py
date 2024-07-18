# Generated by Django 5.0.4 on 2024-07-06 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_task'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.PositiveIntegerField()),
                ('room_type', models.CharField(choices=[('Standard', 'Standard'), ('Deluxe', 'Deluxe'), ('Suite', 'Suite')], max_length=10)),
                ('capacity', models.PositiveIntegerField()),
                ('amenities', models.TextField()),
                ('price_per_night', models.DecimalField(decimal_places=2, max_digits=10)),
                ('is_reserved', models.BooleanField(default=False)),
            ],
        ),
    ]
