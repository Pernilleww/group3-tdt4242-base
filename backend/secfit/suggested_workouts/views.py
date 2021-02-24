from rest_framework.decorators import api_view
from rest_framework.response import Response
from suggested_workouts.models import SuggestedWorkout
from .serializer import SuggestedWorkoutSerializer
from users.models import User


@api_view(['POST'])
def createSuggestedWorkouts(request):
    suggested_workout = SuggestedWorkout
    serializer = SuggestedWorkoutSerializer(data=request.data)

    if serializer.is_valid():
        suggested_workout.objects.create(
            coach=request.user, **serializer.validated_data)
        return Response({"message": "Got some data!", "data": serializer.validated_data})
    return Response({"message": "Something went wrong.", "error": serializer.errors})


@api_view(['GET'])
def listAthleteSuggestedWorkouts(request):
    suggested_workout = SuggestedWorkout.objects.all()
    serializer = SuggestedWorkoutSerializer(suggested_workout, many=True)
    return Response({"message": "Athlete's workout", "data": serializer.data})


@api_view(['GET'])
def listCoachSuggestedWorkouts(request):
    return Response({"message": "Coach's suggested workout!"})
