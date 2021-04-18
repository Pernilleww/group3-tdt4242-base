import os
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth import get_user_model
from suggested_workouts.models import SuggestedWorkout


class Workout(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateTimeField()
    notes = models.TextField()
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="workouts"
    )
    planned = models.BooleanField(default=False)

    PUBLIC = "PU"
    COACH = "CO"
    PRIVATE = "PR"
    VISIBILITY_CHOICES = [
        (PUBLIC, "Public"),
        (COACH, "Coach"),
        (PRIVATE, "Private"),
    ]

    visibility = models.CharField(
        max_length=2, choices=VISIBILITY_CHOICES, default=COACH
    )

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return self.name


def workout_directory_path(instance, filename):
    if instance.workout != None:
        return f"workouts/{instance.workout.id}/{filename}"
    elif instance.suggested_workout != None:
        return f"suggested_workouts/{instance.suggested_workout.id}/{filename}"
    return f"images"


class WorkoutFile(models.Model):
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="files", null=True, blank=True)
    suggested_workout = models.ForeignKey(
        SuggestedWorkout, on_delete=models.CASCADE, related_name="suggested_workout_files", null=True, blank=True)
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="workout_files", null=True, blank=True
    )
    file = models.FileField(upload_to=workout_directory_path)
