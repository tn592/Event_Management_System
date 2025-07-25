# Generated by Django 5.2.4 on 2025-07-05 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="participant",
            name="email",
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name="participant",
            name="name",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
