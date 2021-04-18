from django.shortcuts import render
from rest_framework import generics, mixins
from utils.mixins import CreateListModelMixin
from exercises.serializers import ExerciseInstanceSerializer, ExerciseSerializer
from rest_framework import permissions
from workouts.permissions import IsOwnerOfWorkout
from exercises.models import Exercise, ExerciseInstance
from django.db.models import Q


class ExerciseList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):

    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ExerciseDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ExerciseInstanceList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    CreateListModelMixin,
    generics.GenericAPIView,
):
    serializer_class = ExerciseInstanceSerializer
    permission_classes = [permissions.IsAuthenticated & IsOwnerOfWorkout]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def get_queryset(self):
        qs = ExerciseInstance.objects.filter(
            Q(workout__owner=self.request.user)
            | (
                (Q(workout__visibility="CO") | Q(workout__visibility="PU"))
                & Q(workout__owner__coach=self.request.user)
            ) | (Q(suggested_workout__coach=self.request.user) | Q(suggested_workout__athlete=self.request.user))
        ).distinct()

        return qs


class ExerciseInstanceDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = ExerciseInstance.objects.all()
    serializer_class = ExerciseInstanceSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
