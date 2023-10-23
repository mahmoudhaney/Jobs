# Generated by Django 4.2.6 on 2023-10-22 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import jobs.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('website', models.URLField()),
                ('cv', models.FileField(default='none', upload_to=jobs.models.application_cv_upload)),
                ('cover_letter', models.TextField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicatoin_job', to='jobs.job')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applicatoin_owner', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('job', 'owner')},
            },
        ),
        migrations.DeleteModel(
            name='Candidate',
        ),
    ]
