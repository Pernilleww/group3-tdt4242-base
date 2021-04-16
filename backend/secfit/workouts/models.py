"""Contains the models for the workouts Django application. Users
log workouts (Workout), which contain instances (ExerciseInstance) of various
type of exercises (Exercise). The user can also upload files (WorkoutFile) .
"""
import os
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth import get_user_model
from suggested_workouts.models import SuggestedWorkout


class OverwriteStorage(FileSystemStorage):
    """Filesystem storage for overwriting files. Currently unused."""

    def get_available_name(self, name, max_length=None):
        """https://djangosnippets.org/snippets/976/
        Returns a filename that's free on the target storage system, and
        available for new content to be written to.

        Args:
            name (str): Name of the file
            max_length (int, optional): Maximum length of a file name. Defaults to None.
        """
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

    # Visibility levels
    PUBLIC = "PU"  # Visible to all authenticated users
    COACH = "CO"  # Visible only to owner and their coach
    PRIVATE = "PR"  # Visible only to owner
    VISIBILITY_CHOICES = [
        (PUBLIC, "Public"),
        (COACH, "Coach"),
        (PRIVATE, "Private"),
    ]  # Choices for visibility level

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
    """Return path for which workout files should be uploaded on the web server

    Args:
        instance (WorkoutFile): WorkoutFile instance
        filename (str): Name of the file

    Returns:
        str: Path where workout file is stored
    """
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
