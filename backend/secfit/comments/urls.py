from django.urls import path, include
from comments.views import CommentList, CommentDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("api/comments/", CommentList.as_view(), name="comment-list"),
    path("api/comments/<int:pk>/", CommentDetail.as_view(), name="comment-detail"),
]
