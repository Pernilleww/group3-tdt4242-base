from django.urls import path, include
from suggested_workouts import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("api/suggested-workouts/create/", views.create_suggested_workouts,
         name="suggested_workouts_create"),
    path("api/suggested-workouts/athlete-list/",
         views.list_athlete_suggested_workouts, name="suggested_workouts_for_athlete"),
    path("api/suggested-workouts/coach-list/",
         views.list_coach_suggested_workouts, name="suggested_workouts_by_coach"),
    path("api/suggested-workouts/", views.list_all_suggested_workouts,
         name="list_all_suggested_workouts"),
    path("api/suggested-workout/<int:pk>/",
         views.detailed_suggested_workouts, name="suggested-workout-detail")
]
