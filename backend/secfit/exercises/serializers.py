from rest_framework import serializers
from rest_framework.serializers import HyperlinkedRelatedField
from exercises.models import Exercise, ExerciseInstance
from suggested_workouts.models import SuggestedWorkout
from workouts.models import Workout


class ExerciseInstanceSerializer(serializers.HyperlinkedModelSerializer):
    workout = HyperlinkedRelatedField(
        queryset=Workout.objects.all(), view_name="workout-detail", required=False
    )
    suggested_workout = HyperlinkedRelatedField(queryset=SuggestedWorkout.objects.all(
    ), view_name="suggested-workout-detail", required=False)

    class Meta:
        model = ExerciseInstance
        fields = ["url", "id", "exercise", "sets",
                  "number", "workout", "suggested_workout"]


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    instances = serializers.HyperlinkedRelatedField(
        many=True, view_name="exerciseinstance-detail", read_only=True
    )

    class Meta:
        model = Exercise
        fields = ["url", "id", "name", "description", "unit", "instances"]
