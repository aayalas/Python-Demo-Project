# Generated by Django 4.0 on 2023-03-25 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_rename_is_staff_customuser_admin_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='staff',
            field=models.BooleanField(default=False),
        ),
    ]
