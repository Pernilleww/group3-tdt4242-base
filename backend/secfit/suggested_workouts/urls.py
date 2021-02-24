from django.urls import path, include
from suggested_workouts import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("api/suggested_workouts/create/", views.createSuggestedWorkouts,
         name="suggested_workouts"),
    path("api/suggested_workouts/athlete-list",
         views.listAthleteSuggestedWorkouts, name="suggested_workouts_for_athlete"),
    path("api/suggested_workouts/coach-list",
         views.listCoachSuggestedWorkouts, name="suggested_workouts_by_coach")
]
