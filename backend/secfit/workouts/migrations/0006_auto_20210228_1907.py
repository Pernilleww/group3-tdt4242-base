# Generated by Django 3.1 on 2021-02-28 19:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0005_workoutfile_suggested_workout'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workoutfile',
            name='workout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='workouts.workout'),
        ),
    ]