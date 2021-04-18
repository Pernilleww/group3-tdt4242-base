from rest_framework import generics, mixins
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.parsers import (
    JSONParser,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.db.models import Q
from rest_framework import filters
from workouts.parsers import MultipartJsonParserWorkout
from workouts.permissions import (
    IsOwner,
    IsCoachAndVisibleToCoach,
    IsOwnerOfWorkout,
    IsCoachOfWorkoutAndVisibleToCoach,
    IsReadOnly,
    IsPublic,
    IsWorkoutPublic,
    RememberMePermission
)
from workouts.mixins import CreateListModelMixin
from workouts.models import Workout, WorkoutFile
from workouts.serializers import WorkoutSerializer
from workouts.serializers import WorkoutFileSerializer
from exercises.serializers import ExerciseInstanceSerializer, ExerciseSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import json
from datetime import datetime
import pytz


class WorkoutList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):

    serializer_class = WorkoutSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    parser_classes = [
        MultipartJsonParserWorkout,
        JSONParser,
    ]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["name", "date", "owner__username"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def handleExpiredPlannedWorkouts(self, qs):
        time_now = datetime.now()
        time_now_adjusted = pytz.utc.localize(time_now)
        for i in range(0, len(qs)):
            if qs[i].planned and time_now_adjusted > qs[i].date:
                qs[i].planned = False
                qs[i].save()
        return qs

    def get_queryset(self):
        qs = Workout.objects.filter(
            Q(visibility="PU")
            | Q(owner=self.request.user)
            | (Q(visibility="CO") & Q(owner__coach=self.request.user))
            | (Q(visibility="PR") & Q(owner=self.request.user))
        ).distinct()

        qs = self.handleExpiredPlannedWorkouts(qs)
        return qs


class WorkoutDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & (IsOwner | (IsReadOnly & (IsCoachAndVisibleToCoach | IsPublic)))
    ]
    parser_classes = [MultipartJsonParserWorkout, JSONParser]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class WorkoutFileList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):

    queryset = WorkoutFile.objects.all()
    serializer_class = WorkoutFileSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOfWorkout]
    parser_classes = [MultipartJsonParserWorkout, JSONParser]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        qs = WorkoutFile.objects.filter(
            Q(owner=self.request.user)
            | Q(workout__owner=self.request.user)
            | (
                Q(workout__visibility="CO")
                & Q(workout__owner__coach=self.request.user)
            )
        ).distinct()
        return qs


class WorkoutFileDetail(
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    queryset = WorkoutFile.objects.all()
    serializer_class = WorkoutFileSerializer
    permission_classes = [
        permissions.IsAuthenticated
        & (
            IsOwner
            | IsOwnerOfWorkout
            | (IsReadOnly & (IsCoachOfWorkoutAndVisibleToCoach | IsWorkoutPublic))
        )
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
