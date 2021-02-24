from rest_framework import serializers
from .models import SuggestedWorkout


class SuggestedWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedWorkout
        exclude = ['coach']
