# Generated by Django 3.2.25 on 2024-09-24 16:43

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20240924_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='follows',
            field=models.ManyToManyField(blank=True, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]
