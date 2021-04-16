"""Module for registering models from workouts app to admin page so that they appear
"""
from django.contrib import admin

from .models import SuggestedWorkout

admin.site.register(SuggestedWorkout)

