# Generated by Django 3.1.5 on 2021-06-17 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(blank=True, max_length=255)),
                ('title', models.CharField(blank=True, max_length=255)),
                ('date', models.IntegerField(blank=True, null=True)),
                ('text', models.TextField(blank=True)),
                ('label', models.CharField(blank=True, max_length=255)),
                ('word_count', models.PositiveIntegerField(blank=True, default=None, null=True)),
                ('tokenized_text', models.JSONField(blank=True, default=None, null=True)),
                ('_word_counts_counter', models.JSONField(blank=True, default=dict, null=True)),
                ('_part_of_speech_tags', models.JSONField(blank=True, default=list, null=True)),
            ],
        ),
    ]
