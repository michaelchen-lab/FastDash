# Generated by Django 3.1 on 2020-09-20 09:20

import core_API.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_API', '0003_dataset'),
    ]

    operations = [
        migrations.AddField(
            model_name='dataset',
            name='file',
            field=models.FileField(default='test', upload_to=core_API.utils.upload_file),
            preserve_default=False,
        ),
    ]