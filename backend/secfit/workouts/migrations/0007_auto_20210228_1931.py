# Generated by Django 3.1 on 2021-02-28 19:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workouts', '0006_auto_20210228_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exerciseinstance',
            name='workout',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercise_instances', to='workouts.workout'),
        ),
    ]