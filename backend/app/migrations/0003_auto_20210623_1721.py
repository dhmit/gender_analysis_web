# Generated by Django 3.1.5 on 2021-06-23 17:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_document'),
    ]

    operations = [
        migrations.RenameField(
            model_name='document',
            old_name='date',
            new_name='year',
        ),
    ]
