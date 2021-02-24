from rest_framework.decorators import api_view
from rest_framework.response import Response
from suggested_workouts.models import SuggestedWorkout


@api_view(['POST'])
def createSuggestedWorkouts(request):
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})


@api_view(['GET'])
def listAthleteSuggestedWorkouts(request):
    return Response({"message": "Athlete's workout"})


@api_view(['GET'])
def listCoachSuggestedWorkouts(request):
    return Response({"message": "Coach's suggested workout!"})
