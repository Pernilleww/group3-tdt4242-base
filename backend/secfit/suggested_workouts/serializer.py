from rest_framework import serializer
from .models import SuggestedWorkout


class SuggestedWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuggestedWorkout
        fields = exclude('coach')
