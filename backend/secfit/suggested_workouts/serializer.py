from rest_framework import serializers
from .models import SuggestedWorkout
from users.models import User
from workouts.serializers import WorkoutFileSerializer, ExerciseInstanceSerializer
from workouts.models import ExerciseInstance, WorkoutFile, Exercise


class SuggestedWorkoutSerializer(serializers.ModelSerializer):
    suggested_exercise_instances = ExerciseInstanceSerializer(
        many=True, required=False)
    suggested_workout_files = WorkoutFileSerializer(many=True, required=False)
    coach_username = serializers.SerializerMethodField()

    class Meta:
        model = SuggestedWorkout
        fields = ['id', 'athlete', 'coach_username', 'name', 'notes', 'date',
                  'status', 'coach', 'suggested_exercise_instances', 'suggested_workout_files']
        extra_kwargs = {"coach": {"read_only": True}}

    def create(self, validated_data, coach):
        exercise_instances_data = validated_data.pop(
            'suggested_exercise_instances')
        files_data = []
        if "suggested_workout_files" in validated_data:
            files_data = validated_data.pop("suggested_workout_files")

        suggested_workout = SuggestedWorkout.objects.create(
            coach=coach, **validated_data)

        for exercise_instance_data in exercise_instances_data:
            ExerciseInstance.objects.create(
                suggested_workout=suggested_workout, **exercise_instance_data)
        for file_data in files_data:
            WorkoutFile.objects.create(
                suggested_workout=suggested_workout, owner=suggested_workout.coach, file=file_data.get(
                    "file")
            )

        return suggested_workout

    def update(self, instance, validated_data):
        exercise_instances_data = validated_data.pop(
            "suggested_exercise_instances")
        exercise_instances = instance.suggested_exercise_instances

        instance.name = validated_data.get("name", instance.name)
        instance.notes = validated_data.get("notes", instance.notes)
        instance.status = validated_data.get(
            "status", instance.status)
        instance.date = validated_data.get("date", instance.date)
        instance.athlete = validated_data.get("athlete", instance.athlete)
        instance.save()

        self.handle_exercise_instances(
            exercise_instances, exercise_instances_data, instance)

        self.handle_workout_files(validated_data, instance)

        return instance

    def handle_exercise_instances(self, exercise_instances, exercise_instances_data, instance):

        for exercise_instance, exercise_instance_data in zip(
                exercise_instances.all(), exercise_instances_data):
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

        # Create new exercise instances
        if len(exercise_instances_data) > len(exercise_instances.all()):
            for i in range(len(exercise_instances.all()), len(exercise_instances_data)):
                exercise_instance_data = exercise_instances_data[i]
                ExerciseInstance.objects.create(
                    suggested_workout=instance, **exercise_instance_data
                )
        # Delete exercise instances
        elif len(exercise_instances_data) < len(exercise_instances.all()):
            for i in range(len(exercise_instances_data), len(exercise_instances.all())):
                exercise_instances.all()[i].delete()

    def handle_workout_files(self, validated_data, instance):
        if "suggested_workout_files" in validated_data:
            files_data = validated_data.pop("suggested_workout_files")
            files = instance.suggested_workout_files

            for file, file_data in zip(files.all(), files_data):
                file.file = file_data.get("file", file.file)
                file.save()

            # Create new WorkoutFiles
            if len(files_data) > len(files.all()):
                for i in range(len(files.all()), len(files_data)):
                    WorkoutFile.objects.create(
                        suggested_workout=instance,
                        owner=instance.coach,
                        file=files_data[i].get("file"),
                    )
            # Delete WorkoutFiles
            elif len(files_data) < len(files.all()):
                for i in range(len(files_data), len(files.all())):
                    files.all()[i].delete()

    def get_coach_username(self, obj):
        return obj.coach.username
