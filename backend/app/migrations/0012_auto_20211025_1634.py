# Generated by Django 3.1.5 on 2021-10-25 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_frequencyanalysis'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='new_attributes',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]
