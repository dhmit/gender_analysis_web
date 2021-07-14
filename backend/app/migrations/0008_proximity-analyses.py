# Generated by Django 3.1.5 on 2021-07-14 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_corpus'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProximityAnalyses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word_window', models.PositiveIntegerField()),
                ('results', models.JSONField()),
                ('by_date', models.JSONField(default=dict)),
                ('by_document', models.JSONField(default=dict)),
                ('by_gender', models.JSONField(default=dict)),
                ('by_metadata', models.JSONField(default=dict)),
                ('by_overlap', models.JSONField(default=dict)),
                ('corpus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proximity', to='app.corpus')),
            ],
        ),
    ]