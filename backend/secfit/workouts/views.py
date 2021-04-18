from rest_framework import generics, mixins
from rest_framework import permissions

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
)
from workouts.mixins import CreateListModelMixin
from workouts.models import Workout, Exercise, ExerciseInstance, WorkoutFile
from workouts.serializers import WorkoutSerializer, ExerciseSerializer
from workouts.serializers import RememberMeSerializer
from workouts.serializers import ExerciseInstanceSerializer, WorkoutFileSerializer
from django.core.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
import json
from collections import namedtuple
import base64
import pickle
from django.core.signing import Signer
from datetime import datetime
import pytz


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "workouts": reverse("workout-list", request=request, format=format),
            "exercises": reverse("exercise-list", request=request, format=format),
            "exercise-instances": reverse(
                "exercise-instance-list", request=request, format=format
            ),
            "workout-files": reverse(
                "workout-file-list", request=request, format=format
            ),
            "comments": reverse("comment-list", request=request, format=format),
            "likes": reverse("like-list", request=request, format=format),
        }
    )


class RememberMe(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):

    serializer_class = RememberMeSerializer

    def get(self, request):
        if request.user.is_authenticated == False:
            raise PermissionDenied
        else:
            return Response({"remember_me": self.rememberme()})

    def post(self, request):
        cookieObject = namedtuple("Cookies", request.COOKIES.keys())(
            *request.COOKIES.values()
        )
        user = self.get_user(cookieObject)
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
        )

    def get_user(self, cookieObject):
        decode = base64.b64decode(cookieObject.remember_me)
        user, sign = pickle.loads(decode)

        if sign == self.sign_user(user):
            return user

    def rememberme(self):
        creds = [self.request.user, self.sign_user(str(self.request.user))]
        return base64.b64encode(pickle.dumps(creds))

    def sign_user(self, username):
        signer = Signer()
        signed_user = signer.sign(username)
        return signed_user


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
        timeNow = datetime.now()
        timeNowAdjusted = pytz.utc.localize(timeNow)
        for i in range(0, len(qs)):
            if qs[i].planned and timeNowAdjusted > qs[i].date:
                qs[i].planned = False
                qs[i].save()
        return qs

    def get_queryset(self):
        qs = Workout.objects.none()
        if self.request.user:
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
        qs = ExerciseInstance.objects.none()
        if self.request.user:
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
        qs = WorkoutFile.objects.none()
        if self.request.user:
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
    mixins.UpdateModelMixin,
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
