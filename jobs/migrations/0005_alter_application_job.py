# Generated by Django 4.2.6 on 2023-10-23 04:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0004_alter_application_job'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='jobs.job'),
        ),
    ]
