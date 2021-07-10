# Generated by Django 3.1.5 on 2021-07-10 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20210709_1639'),
    ]

    operations = [
        migrations.AddField(
            model_name='character',
            name='coref_clusters',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='count',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='first_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='character',
            name='full_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='character',
            name='gender',
            field=models.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='honorifics',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='last_name',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='character',
            name='main_title',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='character',
            name='mentions',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='character',
            name='middle_name',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
