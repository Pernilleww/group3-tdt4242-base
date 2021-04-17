import os
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth import get_user_model
from suggested_workouts.models import SuggestedWorkout


class OverwriteStorage(FileSystemStorage):
    """Currently unused."""

    def get_available_name(self, name, max_length=None):
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))


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


class RememberMe(models.Model):
    remember_me = models.CharField(max_length=500)

    def __str__(self):
        return self.remember_me
