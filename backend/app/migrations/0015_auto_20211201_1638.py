# Generated by Django 3.1.5 on 2021-12-01 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0014_auto_20211201_1636'),
    ]

    operations = [
        migrations.AlterField(
            model_name='distinctivenessanalysis',
            name='results',
            field=models.JSONField(null=True),
        ),
    ]