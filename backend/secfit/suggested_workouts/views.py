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
        print(request.user.coach)
        # Denne printer ikke ut noen ting? Burde gi en liste over alle athletes...
        print(request.user.athletes)
        if(not request.user.athletes or chosen_athlete not in request.user.athletes):
            return Response({"message": "You can not assign the workout to someone who is not your athlete."}, status=status.HTTP_400_BAD_REQUEST)
        SuggestedWorkout.objects.create(
            coach=request.user, **serializer.validated_data)
        return Response({"message": "Suggested workout successfully created!"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Something went wrong.", "error": serializer.errors})


@api_view(['GET'])
def listAthleteSuggestedWorkouts(request):
    # Henter ut riktige workouts gitt brukeren som sender requesten
    suggested_workouts = SuggestedWorkout.objects.filter(athlete=request.user)
    serializer = SuggestedWorkoutSerializer(suggested_workouts, many=True)
    return Response({"message": "Suggested workouts to you (athlete)", "data": serializer.data}, status=status.HTTP_200_OK)


@api_view(['GET'])
def listCoachSuggestedWorkouts(request):
    # Gjør spørring på workouts der request.user er coach
    suggested_workouts = SuggestedWorkout.objects.filter(coach=request.user)
    serializer = SuggestedWorkoutSerializer(suggested_workouts, many=True)
    return Response({"message": "Suggested workouts from you (coach)", "data": serializer.data}, status=status.HTTP_200_OK)
