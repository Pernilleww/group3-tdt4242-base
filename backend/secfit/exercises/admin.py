from django.contrib import admin
from exercises.models import ExerciseInstance, Exercise

admin.site.register(Exercise)
admin.site.register(ExerciseInstance)
