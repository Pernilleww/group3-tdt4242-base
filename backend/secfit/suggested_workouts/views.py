from rest_framework.decorators import api_view
from suggested_workouts.models import SuggestedWorkout
from .serializer import SuggestedWorkoutSerializer
from users.models import User
from rest_framework import status
from rest_framework.response import Response

"""
Handling post request of a new suggested workout instance.
"""


@api_view(['POST'])
def createSuggestedWorkouts(request):
    serializer = SuggestedWorkoutSerializer(data=request.data)
    if serializer.is_valid():
        chosen_athlete_id = request.data['athlete']
        chosen_athlete = User.objects.get(id=chosen_athlete_id)
        if(request.user != chosen_athlete.coach):
            return Response({"message": "You can not assign the workout to someone who is not your athlete."}, status=status.HTTP_400_BAD_REQUEST)
        SuggestedWorkout.objects.create(
            coach=request.user, **serializer.validated_data)
        return Response({"message": "Suggested workout successfully created!"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Something went wrong.", "error": serializer.errors})


@api_view(['GET'])
def listAthleteSuggestedWorkouts(request):
    # Henter ut riktige workouts gitt brukeren som sender requesten
    suggested_workouts = SuggestedWorkout.objects.filter(athlete=request.user)
    if not request.user:
        return Response({"message": "You have to log in to see this information."}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = SuggestedWorkoutSerializer(suggested_workouts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def listCoachSuggestedWorkouts(request):
    # Gjør spørring på workouts der request.user er coach
    if not request.user:
        return Response({"message": "You have to log in to see this information."}, status=status.HTTP_401_UNAUTHORIZED)
    suggested_workouts = SuggestedWorkout.objects.filter(coach=request.user)
    serializer = SuggestedWorkoutSerializer(suggested_workouts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['PUT'])
def updateSuggestedWorkout(request, pk):
    suggested_workouts = SuggestedWorkout.objects.get(id=pk)
    serializer = SuggestedWorkoutSerializer(
        suggested_workouts, data=request.data)
    if(serializer.is_valid()):
        serializer.save()
        return Response({"message": "Successfully updated the suggested workout!"}, status=status.HTTP_200_OK)
    return Response({"message": "Something went wrong.", "error": serializer.errors}, status=HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listAllSuggestedWorkouts(request):
    # Lister alle workouts som er foreslått
    suggested_workouts = SuggestedWorkout.objects.all()
    serializer = SuggestedWorkoutSerializer(suggested_workouts, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)
