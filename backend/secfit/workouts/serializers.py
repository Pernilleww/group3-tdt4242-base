"""Serializers for the workouts application
"""
from rest_framework import serializers
from rest_framework.serializers import HyperlinkedRelatedField
from workouts.models import Workout, Exercise, ExerciseInstance, WorkoutFile, RememberMe
from datetime import datetime
import pytz
from suggested_workouts.models import SuggestedWorkout


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


class WorkoutFileSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    workout = HyperlinkedRelatedField(
        queryset=Workout.objects.all(), view_name="workout-detail", required=False
    )
    suggested_workout = HyperlinkedRelatedField(
        queryset=SuggestedWorkout.objects.all(), view_name="suggested-workout-detail", required=False
    )

    class Meta:
        model = WorkoutFile
        fields = ["url", "id", "owner", "file", "workout", "suggested_workout"]


class WorkoutSerializer(serializers.HyperlinkedModelSerializer):
    owner_username = serializers.SerializerMethodField()
    exercise_instances = ExerciseInstanceSerializer(many=True, required=True)
    files = WorkoutFileSerializer(many=True, required=False)

    class Meta:
        model = Workout
        fields = [
            "url",
            "id",
            "name",
            "date",
            "notes",
            "owner",
            "planned",
            "owner_username",
            "visibility",
            "exercise_instances",
            "files",
        ]
        extra_kwargs = {"owner": {"read_only": True}}

    def check_date(self, validated_data):
        time_now = datetime.now()
        time_now_adjusted = pytz.utc.localize(time_now)

        if validated_data["planned"]:
            if time_now_adjusted >= validated_data["date"]:
                raise serializers.ValidationError(
                    {"date": ["Date must be a future date"]})
        else:
            if time_now_adjusted <= validated_data["date"]:
                raise serializers.ValidationError(
                    {"date": ["Date must be an old date"]})

    def create(self, validated_data):
        self.check_date(validated_data)

        exercise_instances_data = validated_data.pop("exercise_instances")
        files_data = []
        if "files" in validated_data:
            files_data = validated_data.pop("files")

        workout = Workout.objects.create(**validated_data)

        for exercise_instance_data in exercise_instances_data:
            ExerciseInstance.objects.create(
                workout=workout, **exercise_instance_data)
        for file_data in files_data:
            WorkoutFile.objects.create(
                workout=workout, owner=workout.owner, file=file_data.get(
                    "file")
            )

        return workout

    def update(self, instance, validated_data):
        self.check_date(validated_data)

        exercise_instances_data = validated_data.pop("exercise_instances")
        exercise_instances = instance.exercise_instances

        instance.name = validated_data.get("name", instance.name)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.visibility = validated_data.get(
            "visibility", instance.visibility)
        instance.date = validated_data.get("date", instance.date)
        instance.save()

        self.handle_exercise_instances(
            exercise_instances, exercise_instances_data, instance)

        self.handle_workout_files(validated_data, instance)

        return instance

    def handle_exercise_instances(self, exercise_instances, exercise_instances_data, instance):
        for exercise_instance, exercise_instance_data in zip(
            exercise_instances.all(), exercise_instances_data
        ):
            exercise_instance.exercise = exercise_instance_data.get(
                "exercise", exercise_instance.exercise
            )
            exercise_instance.number = exercise_instance_data.get(
                "number", exercise_instance.number
            )
            exercise_instance.sets = exercise_instance_data.get(
                "sets", exercise_instance.sets
            )
            exercise_instance.save()

        # If new exercise instances have been added to the workout, then create them
        if len(exercise_instances_data) > len(exercise_instances.all()):
            for i in range(len(exercise_instances.all()), len(exercise_instances_data)):
                exercise_instance_data = exercise_instances_data[i]
                ExerciseInstance.objects.create(
                    workout=instance, **exercise_instance_data
                )
        # Else if exercise instances have been removed from the workout, then delete them
        elif len(exercise_instances_data) < len(exercise_instances.all()):
            for i in range(len(exercise_instances_data), len(exercise_instances.all())):
                exercise_instances.all()[i].delete()

    def handle_workout_files(self, validated_data, instance):
        if "files" in validated_data:
            files_data = validated_data.pop("files")
            files = instance.files
            for file, file_data in zip(files.all(), files_data):

                file.file = file_data.get("file", file.file)
                file.save()

            # If new files have been added, creating new WorkoutFiles
            if len(files_data) > len(files.all()):
                for i in range(len(files.all()), len(files_data)):
                    WorkoutFile.objects.create(
                        workout=instance,
                        owner=instance.owner,
                        file=files_data[i].get("file"),
                    )
            # Else if files have been removed, delete WorkoutFiles
            elif len(files_data) < len(files.all()):
                for i in range(len(files_data), len(files.all())):
                    files.all()[i].delete()

    def get_owner_username(self, obj):
        return obj.owner.username


class ExerciseSerializer(serializers.HyperlinkedModelSerializer):
    instances = serializers.HyperlinkedRelatedField(
        many=True, view_name="exerciseinstance-detail", read_only=True
    )

    class Meta:
        model = Exercise
        fields = ["url", "id", "name", "description", "unit", "instances"]


class RememberMeSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RememberMe
        fields = ["remember_me"]
