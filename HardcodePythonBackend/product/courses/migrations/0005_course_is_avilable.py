# Generated by Django 4.2.10 on 2024-08-20 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_alter_lesson_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='is_avilable',
            field=models.BooleanField(blank=True, default=True, verbose_name='Доступность'),
            preserve_default=False,
        ),
    ]
