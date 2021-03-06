# Generated by Django 3.1 on 2021-04-18 17:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('suggested_workouts', '0002_auto_20210418_1749'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workouts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='exerciseinstance',
            name='suggested_workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_exercise_instances', to='suggested_workouts.suggestedworkout'),
        ),
        migrations.AddField(
            model_name='workout',
            name='planned',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='workoutfile',
            name='suggested_workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='suggested_workout_files', to='suggested_workouts.suggestedworkout'),
        ),
        migrations.AlterField(
            model_name='exerciseinstance',
            name='workout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise_instances', to='workouts.workout'),
        ),
        migrations.AlterField(
            model_name='workoutfile',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='workout_files', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='workoutfile',
            name='workout',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='workouts.workout'),
        ),
    ]
