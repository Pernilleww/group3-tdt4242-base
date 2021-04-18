from django.db import models
from suggested_workouts.models import SuggestedWorkout
from workouts.models import Workout


class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class ExerciseInstance(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="exercise_instances", null=True
    )
    suggested_workout = models.ForeignKey(
        SuggestedWorkout, on_delete=models.CASCADE, related_name="suggested_exercise_instances", null=True, blank=True)
    exercise = models.ForeignKey(
        Exercise, on_delete=models.CASCADE, related_name="instances"
    )
    sets = models.IntegerField()
    number = models.IntegerField()
