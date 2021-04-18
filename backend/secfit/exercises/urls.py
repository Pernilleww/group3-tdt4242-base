from django.urls import path, include
from exercises import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns(
    [path("api/exercises/", views.ExerciseList.as_view(), name="exercise-list"),
     path("api/exercises/<int:pk>/",
          views.ExerciseDetail.as_view(), name="exercise-detail"),
     path("api/exercise-instances/", views.ExerciseInstanceList.as_view(),
          name="exercise-instance-list"),
     path("api/exercise-instances/<int:pk>/",
          views.ExerciseInstanceDetail.as_view(), name="exerciseinstance-detail"),
     ]
)
