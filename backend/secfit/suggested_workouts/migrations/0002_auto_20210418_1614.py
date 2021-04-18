# Generated by Django 3.1 on 2021-04-18 16:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('suggested_workouts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='suggestedworkout',
            name='visibility',
        ),
        migrations.AddField(
            model_name='suggestedworkout',
            name='status',
            field=models.CharField(choices=[('a', 'Accepted'), ('p', 'Pending'), ('d', 'Declined')], default='p', max_length=8),
        ),
        migrations.AlterField(
            model_name='suggestedworkout',
            name='athlete',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='athlete_suggested_workouts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='suggestedworkout',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='coach_suggested_workouts', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='WorkoutRequest',
        ),
    ]
