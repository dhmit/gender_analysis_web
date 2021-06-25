# Generated by Django 3.1.5 on 2021-06-25 17:10

import app.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='PronounSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=60)),
                ('obj', app.fields.LowercaseCharField(max_length=40)),
                ('pos_det', app.fields.LowercaseCharField(max_length=40)),
                ('pos_pro', app.fields.LowercaseCharField(max_length=40)),
                ('reflex', app.fields.LowercaseCharField(max_length=40)),
                ('subj', app.fields.LowercaseCharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Name',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', app.fields.LowercaseCharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='NameSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=60)),
                ('pronoun_series', models.ManyToManyField(to='app.PronounSeries')),
            ],
        ),
        migrations.DeleteModel(
            name='Pronoun',
        ),
        migrations.DeleteModel(
            name='Name',
        ),
        migrations.DeleteModel(
            name='NameSeries',
        ),
    ]
