# Generated by Django 5.0.7 on 2024-08-14 07:15
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0007_remove_menuitem_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='menu',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='menu.menu'),
        ),
    ]
