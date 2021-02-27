from django.urls import path, include
from suggested_workouts import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path("api/suggested-workouts/create/", views.createSuggestedWorkouts,
         name="suggested_workouts"),
    path("api/suggested-workouts/athlete-list",
         views.listAthleteSuggestedWorkouts, name="suggested_workouts_for_athlete"),
    path("api/suggested-workouts/coach-list",
         views.listCoachSuggestedWorkouts, name="suggested_workouts_by_coach"),
    path("api/suggested-workout/update/<int:pk>", views.updateSuggestedWorkout,
         name="update_date_for_suggested_workout"),
    path("api/suggested-workouts", views.listAllSuggestedWorkouts,
         name="list_all_suggested_workouts"),
]
