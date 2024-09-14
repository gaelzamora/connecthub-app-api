# Generated by Django 3.2.25 on 2024-09-14 20:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_alter_project_technologies'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(blank=True, related_name='project_technologie', to='core.Technologie'),
        ),
    ]