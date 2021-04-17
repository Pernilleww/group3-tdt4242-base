from django.shortcuts import render
from rest_framework import generics, mixins
from comments.models import Comment, Like
from rest_framework import permissions
from comments.permissions import IsCommentVisibleToUser
from workouts.permissions import IsOwner, IsReadOnly
from comments.serializers import CommentSerializer, LikeSerializer
from django.db.models import Q
from rest_framework.filters import OrderingFilter

# Create your views here.


class CommentList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ["timestamp"]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        if self.request.user:
            """A comment should be visible to the requesting user if any of the following hold:
            - The comment is on a public visibility workout
            - The comment was written by the user
            - The comment is on a coach visibility workout and the user is the workout owner's coach
            - The comment is on a workout owned by the user
            """
            # The code below is kind of duplicate of the one in ./permissions.py
            # We should replace it with a better solution.
            # Or maybe not.

            qs = Comment.objects.filter(
                Q(workout__visibility="PU")
                | Q(owner=self.request.user)
                | (
                    Q(workout__visibility="CO")
                    & Q(workout__owner__coach=self.request.user)
                )
                | Q(workout__owner=self.request.user)
            ).distinct()

        return qs

# Details of comment


class CommentDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticated & IsCommentVisibleToUser & (
            IsOwner | IsReadOnly)
    ]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# List of likes
class LikeList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Like.objects.filter(owner=self.request.user)


# Details of like
class LikeDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [permissions.IsAuthenticated]
    _Detail = []

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
