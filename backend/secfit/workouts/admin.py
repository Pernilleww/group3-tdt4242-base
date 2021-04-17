from django.contrib import admin

from .models import Exercise, ExerciseInstance, Workout, WorkoutFile

admin.site.register(Exercise)
admin.site.register(ExerciseInstance)
admin.site.register(Workout)
admin.site.register(WorkoutFile)

