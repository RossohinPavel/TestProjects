# Generated by Django 5.0.7 on 2024-07-20 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_city_country_delete_statistics_city_country'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='country',
            name='count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
