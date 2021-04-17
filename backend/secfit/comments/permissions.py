from rest_framework import permissions


class IsCommentVisibleToUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.workout.visibility == "PU"
            or obj.owner == request.user
            or (obj.workout.visibility == "CO" and obj.owner.coach == request.user)
            or obj.workout.owner == request.user
        )
