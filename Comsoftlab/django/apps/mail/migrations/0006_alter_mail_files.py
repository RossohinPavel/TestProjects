# Generated by Django 5.1 on 2024-09-13 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mail', '0005_alter_mail_mail_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='files',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
