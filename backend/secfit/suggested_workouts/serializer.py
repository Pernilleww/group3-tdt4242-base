from rest_framework import serializers
from .models import SuggestedWorkout
from users.models import User
from workouts.serializers import WorkoutFileSerializer


class SuggestedWorkoutSerializer(serializers.ModelSerializer):

    class Meta:
        model = SuggestedWorkout
        suggested_workout_files = WorkoutFileSerializer(
            many=True, required=False)
        fields = ['id', 'athlete', 'name', 'notes', 'date',
                  'status', 'suggested_exercise_instances', 'suggested_workout_files']
