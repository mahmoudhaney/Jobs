# Generated by Django 4.2.6 on 2023-10-17 15:12

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default=None, upload_to=accounts.models.user_image_upload),
        ),
    ]
