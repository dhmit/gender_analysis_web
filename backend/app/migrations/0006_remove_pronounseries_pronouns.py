# Generated by Django 3.1.5 on 2021-06-23 22:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_change_pronounseries'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pronounseries',
            name='pronouns',
        ),
    ]
