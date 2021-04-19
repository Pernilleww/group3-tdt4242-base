from django.urls import path, include
from workouts import views
from rest_framework.urlpatterns import format_suffix_patterns


urlpatterns = format_suffix_patterns(
    [
        path("api/workouts/", views.WorkoutList.as_view(), name="workout-list"),
        path(
            "api/workouts/<int:pk>/",
            views.WorkoutDetail.as_view(),
            name="workout-detail",
        ),
        path(
            "api/workout-files/",
            views.WorkoutFileList.as_view(),
            name="workout-file-list",
        ),
        path(
            "api/workout-files/<int:pk>/",
            views.WorkoutFileDetail.as_view(),
            name="workoutfile-detail",
        ),
    ]
)
