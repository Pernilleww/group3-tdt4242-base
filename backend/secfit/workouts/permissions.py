"""Contains custom DRF permissions classes for the workouts app
"""
from rest_framework import permissions
from workouts.models import Workout


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsOwnerOfWorkout(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.data.get("workout"):
                workout_id = request.data["workout"].split("/")[-2]
                workout = Workout.objects.get(pk=workout_id)
                if workout:
                    return workout.owner == request.user
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return obj.workout.owner == request.user


class IsCoachAndVisibleToCoach(permissions.BasePermission):
    # Fixed bug where the function did not check for the visibility level

    def has_object_permission(self, request, view, obj):
        return obj.owner.coach == request.user and (obj.visibility == 'PU' or obj.visibility == 'CO')


class IsCoachOfWorkoutAndVisibleToCoach(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Fixed bug where the function did not check for the visibility level
        return obj.workout.owner.coach == request.user and (
            obj.workout.visibility == "PU" or obj.workout.visibility == "CO"
        )


class IsPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.visibility == "PU"


class IsWorkoutPublic(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.workout.visibility == "PU"


class IsReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
