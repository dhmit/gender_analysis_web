# Generated by Django 3.1.5 on 2021-12-01 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20211122_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frequencyanalysis',
            name='results',
            field=models.JSONField(null=True),
        ),
    ]