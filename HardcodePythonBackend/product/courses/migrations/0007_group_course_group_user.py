# Generated by Django 4.2.10 on 2024-08-20 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('courses', '0006_alter_course_is_avilable'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='course',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='group', to='courses.course'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='group',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='group', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
