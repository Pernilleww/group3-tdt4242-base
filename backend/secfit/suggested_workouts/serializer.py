from rest_framework import serializers
from .models import SuggestedWorkout
from users.models import User
from workouts.serializers import WorkoutFileSerializer, ExerciseInstanceSerializer


class SuggestedWorkoutSerializer(serializers.ModelSerializer):
    suggested_exercise_instances = ExerciseInstanceSerializer(
        many=True, required=False)
    suggested_workout_files = WorkoutFileSerializer(
        many=True, required=False)

    class Meta:
        model = SuggestedWorkout
        fields = ['id', 'athlete', 'name', 'notes', 'date',
                  'status', 'suggested_exercise_instances', 'suggested_workout_files']
