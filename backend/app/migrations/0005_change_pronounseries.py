import app.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_name_nameseries'),
    ]

    operations = [
        migrations.AddField(
            model_name='pronounseries',
            name='obj',
            field=app.fields.LowercaseCharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='pronounseries',
            name='pos_det',
            field=app.fields.LowercaseCharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='pronounseries',
            name='pos_pro',
            field=app.fields.LowercaseCharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='pronounseries',
            name='reflex',
            field=app.fields.LowercaseCharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='pronounseries',
            name='subj',
            field=app.fields.LowercaseCharField(blank=True, max_length=40),
        ),
    ]
