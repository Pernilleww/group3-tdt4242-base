from rest_framework import permissions
from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied


class IsCurrentUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class IsAthlete(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.data.get("athlete"):
                athlete_id = request.data["athlete"].split("/")[-2]
                return athlete_id == request.user.id
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.athlete


class IsCoach(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            if request.data.get("athlete"):
                athlete_id = request.data["athlete"].split("/")[-2]
                athlete = get_user_model().objects.get(pk=athlete_id)
                return athlete.coach == request.user
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return request.user == obj.athlete.coach


class RememberMePermission():
    def has_permission(self, request):
        if not request.user.is_authenticated:
            raise PermissionDenied
        return True
