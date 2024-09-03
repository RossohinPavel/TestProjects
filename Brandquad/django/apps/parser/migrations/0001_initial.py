# Generated by Django 5.1 on 2024-08-22 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField()),
                ('date', models.DateTimeField()),
                ('method', models.CharField(max_length=10)),
                ('uri', models.URLField()),
                ('status_code', models.PositiveSmallIntegerField()),
                ('content_length', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
