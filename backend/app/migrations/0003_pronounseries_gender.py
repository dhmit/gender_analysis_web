from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_document')
    ]

    operations = [
        migrations.CreateModel(
            name='PronounSeries',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=60)),
                ('pronouns', models.ManyToManyField(to='app.Pronoun')),
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
    ]
