from django.shortcuts import render
from rest_framework import generics, mixins
from comments.models import Comment
from rest_framework import permissions
from comments.permissions import IsCommentVisibleToUser
from workouts.permissions import IsOwner, IsReadOnly
from comments.serializers import CommentSerializer
from django.db.models import Q
from rest_framework.filters import OrderingFilter


class CommentList(
    mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView
):
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
        queryset = Comment.objects.all()
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
