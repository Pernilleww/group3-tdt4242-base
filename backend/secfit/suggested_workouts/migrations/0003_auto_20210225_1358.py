# Generated by Django 3.1 on 2021-02-25 13:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('suggested_workouts', '0002_suggestedworkout_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='suggestedworkout',
            name='coach',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to=settings.AUTH_USER_MODEL),
        ),
    ]
