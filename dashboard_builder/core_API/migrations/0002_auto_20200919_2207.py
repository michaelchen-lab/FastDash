# Generated by Django 3.1 on 2020-09-19 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core_API', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboard',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
