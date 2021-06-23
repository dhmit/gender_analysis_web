import app.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_pronounseries_gender'),
    ]

    operations = [
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
                ('names', models.ManyToManyField(to='app.Name')),
            ],
        ),
        migrations.AddField(
            model_name='gender',
            name='names_series',
            field=models.ManyToManyField(to='app.NameSeries'),
        ),
    ]