from rest_framework.decorators import api_view
from rest_framework.response import Response
from suggested_workouts.models import SuggestedWorkout
from .serializer import SuggestedWorkoutSerializer
from users.models import User
from rest_framework import status

"""
Handling post request of a new suggested workout instance.
"""


@api_view(['POST'])
def createSuggestedWorkouts(request):
    serializer = SuggestedWorkoutSerializer(data=request.data)
    if serializer.is_valid():
        chosen_athlete = request.data['athlete']
        print(request.user)
        print(request.user.id)
        print(request.user.coach)
        print(request.user.athletes)
        # if(chosen_athlete not in request.user.athletes):
        #     return Response({"message": "You can not assign the workout to someone who is not your athlete."}, status=status.HTTP_400_BAD_REQUEST)
        SuggestedWorkout.objects.create(
            coach=request.user, **serializer.validated_data)
        return Response(status=status.HTTP_201_CREATED)
    return Response({"message": "Something went wrong.", "error": serializer.errors})


@api_view(['GET'])
def listAthleteSuggestedWorkouts(request):
    suggested_workout = SuggestedWorkout.objects.all()
    serializer = SuggestedWorkoutSerializer(suggested_workout, many=True)
    return Response({"message": "Athlete's workout", "data": serializer.data})


@api_view(['GET'])
def listCoachSuggestedWorkouts(request):
    return Response({"message": "Coach's suggested workout!"})
