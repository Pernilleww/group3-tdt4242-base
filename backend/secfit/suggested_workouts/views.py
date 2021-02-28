from rest_framework.decorators import api_view
from suggested_workouts.models import SuggestedWorkout
from .serializer import SuggestedWorkoutSerializer
from users.models import User
from rest_framework import status
from rest_framework.response import Response
from workouts.parsers import MultipartJsonParser
from rest_framework.parsers import (
    JSONParser
)
from rest_framework.decorators import parser_classes
"""
Handling post request of a new suggested workout instance. Handling update, delete and list exercises as well.
"""


@api_view(['POST'])
@parser_classes([MultipartJsonParser,
                 JSONParser])
def createSuggestedWorkouts(request):
    serializer = SuggestedWorkoutSerializer(data=request.data)
    if serializer.is_valid():
        chosen_athlete_id = request.data['athlete']
        chosen_athlete = User.objects.get(id=chosen_athlete_id)
        if(request.user != chosen_athlete.coach):
            return Response({"message": "You can not assign the workout to someone who is not your athlete."}, status=status.HTTP_400_BAD_REQUEST)
        # new_suggested_workout = SuggestedWorkout.objects.create(
        #    coach=request.user, **serializer.validated_data)
        serializer.create(
            validated_data=serializer.validated_data, coach=request.user)
        return Response({"message": "Suggested workout successfully created!"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Something went wrong.", "error": serializer.errors})


@api_view(['GET'])
def listAthleteSuggestedWorkouts(request):
    # Henter ut riktige workouts gitt brukeren som sender requesten
    suggested_workouts = SuggestedWorkout.objects.filter(athlete=request.user)
    if not request.user:
        return Response({"message": "You have to log in to see this information."}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = SuggestedWorkoutSerializer(
        suggested_workouts, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def listCoachSuggestedWorkouts(request):
    # Gjør spørring på workouts der request.user er coach
    if not request.user:
        return Response({"message": "You have to log in to see this information."}, status=status.HTTP_401_UNAUTHORIZED)
    suggested_workouts = SuggestedWorkout.objects.filter(coach=request.user)
    serializer = SuggestedWorkoutSerializer(
        suggested_workouts, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def listAllSuggestedWorkouts(request):
    # Lister alle workouts som er foreslått
    suggested_workouts = SuggestedWorkout.objects.all()
    serializer = SuggestedWorkoutSerializer(
        suggested_workouts, many=True, context={'request': request})
    if not request.user.id:
        return Response({"message": "You have to log in to see this information."}, status=status.HTTP_401_UNAUTHORIZED)
    # elif((request.user.id,) not in list(SuggestedWorkout.objects.values_list('coach')) or (request.user.id,) not in list(SuggestedWorkout.objects.values_list('athlete'))):
    #     return Response({"message": "You must either be a coach or athlete of the suggested workouts to see this information."}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


"""
View for both deleting,updating and retrieving a single workout.
"""


@api_view(['GET', 'DELETE', 'PUT'])
@parser_classes([MultipartJsonParser,
                 JSONParser])
def detailedSuggestedWorkout(request, pk):
    detailed_suggested_workout = SuggestedWorkout.objects.get(id=pk)
    if not request.user.id:
        return Response({"message": "Access denied."}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'GET':
        serializer = SuggestedWorkoutSerializer(
            detailed_suggested_workout, context={'request': request})
        if(request.user.id != detailed_suggested_workout.coach.id and request.user.id != detailed_suggested_workout.athlete.id):
            return Response({"messages": "You have to be a coach or athlete to see this information."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if(request.user.id != detailed_suggested_workout.coach.id and request.user.id != detailed_suggested_workout.athlete.id):
            return Response({"messages": "You have to be a coach or athlete to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)
        SuggestedWorkout.delete(detailed_suggested_workout)
        return Response({"message": "Suggested workout successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        if(request.user.id != detailed_suggested_workout.coach.id and request.user.id != detailed_suggested_workout.athlete.id):
            return Response({"messages": "You have to be a coach or athlete to perform this action."}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = SuggestedWorkoutSerializer(
            detailed_suggested_workout, data=request.data)
        if(serializer.is_valid()):
            serializer.update(instance=detailed_suggested_workout,
                              validated_data=serializer.validated_data)
            return Response({"message": "Successfully updated the suggested workout!"}, status=status.HTTP_200_OK)
        return Response({"message": "Something went wrong.", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
