# Generated by Django 3.1.5 on 2021-07-10 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20210709_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='common_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]