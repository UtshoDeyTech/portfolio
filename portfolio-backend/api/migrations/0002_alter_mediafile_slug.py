# Generated migration for MediaFile slug field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediafile',
            name='slug',
            field=models.SlugField(blank=True, db_index=True, help_text='Custom URL slug for accessing this file. Leave blank to auto-generate.', max_length=255, unique=True),
        ),
    ]
