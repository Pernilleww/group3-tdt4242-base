from django.apps import AppConfig
from .models import Exercise, ExerciseInstance


class ExercisesConfig(AppConfig):
    name = 'exercises'
