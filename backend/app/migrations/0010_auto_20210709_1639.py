# Generated by Django 3.1.5 on 2021-07-09 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20210709_1634'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alias',
            name='author',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='new_attributes',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='part_of_speech_tags',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='text',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='title',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='tokenized_text',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='word_count',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='word_count_counter',
        ),
        migrations.RemoveField(
            model_name='alias',
            name='year',
        ),
        migrations.AddField(
            model_name='alias',
            name='pronoun_rates',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='alias',
            name='raw_pronouns',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AddField(
            model_name='alias',
            name='sanitized_pronoun_rates',
            field=models.JSONField(blank=True, default=list, null=True),
        ),
    ]