# Generated by Django 4.0 on 2023-04-11 00:42

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pro', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='country',
            field=django_countries.fields.CountryField(blank=True, max_length=2, null=True),
        ),
    ]
