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
from django.shortcuts import get_object_or_404

response_messages = {
    "error_not_your_athlete": "You can not assign the workout to someone who is not your athlete.",
    "something_went_wrong": "Something went wrong.",
    "you_have_to_log_in": "You have to log in to see this information.",
    "access_denied": "Access denied.",
    "must_be_coach_or_athlete_info": "You have to be a coach or athlete to see this information.",
    "must_be_coach_or_athlete_action": "You have to be a coach or athlete to perform this action.",
    "suggested_workout_created": "Suggested workout successfully created!",
    "suggested_workout_deleted": "Suggested workout successfully deleted.",
    "suggested_workout_updated": "Successfully updated the suggested workout!"
}


@api_view(['POST'])
@parser_classes([MultipartJsonParser,
                 JSONParser])
def createSuggestedWorkouts(request):
    serializer = SuggestedWorkoutSerializer(data=request.data)
    if serializer.is_valid():
        chosen_athlete_id = request.data['athlete']
        chosen_athlete = User.objects.get(id=chosen_athlete_id)
        if(request.user != chosen_athlete.coach):
            return Response({"message": response_messages["error_not_your_athlete"]}, status=status.HTTP_401_UNAUTHORIZED)

        serializer.create(
            validated_data=serializer.validated_data, coach=request.user)
        return Response({"message": response_messages["suggested_workout_created"]}, status=status.HTTP_201_CREATED)
    return Response({"message": response_messages["something_went_wrong"], "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def listAthleteSuggestedWorkouts(request):
    suggested_workouts = SuggestedWorkout.objects.filter(athlete=request.user)
    if not request.user:
        return Response({"message": response_messages["you_have_to_log_in"]}, status=status.HTTP_401_UNAUTHORIZED)
    serializer = SuggestedWorkoutSerializer(
        suggested_workouts, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def listCoachSuggestedWorkouts(request):
    if not request.user:
        return Response({"message": response_messages["you_have_to_log_in"]}, status=status.HTTP_401_UNAUTHORIZED)
    suggested_workouts = SuggestedWorkout.objects.filter(coach=request.user)
    serializer = SuggestedWorkoutSerializer(
        suggested_workouts, many=True, context={'request': request})
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def listAllSuggestedWorkouts(request):
    suggested_workouts = SuggestedWorkout.objects.all()
    serializer = SuggestedWorkoutSerializer(
        suggested_workouts, many=True, context={'request': request})
    if not request.user.id:
        return Response({"message": response_messages["you_have_to_log_in"]}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT'])
@parser_classes([MultipartJsonParser,
                 JSONParser])
def detailedSuggestedWorkout(request, pk):
    detailed_suggested_workout = get_object_or_404(SuggestedWorkout, pk=pk)
    if not request.user.id:
        return Response({"message": response_messages["access_denied"]}, status=status.HTTP_401_UNAUTHORIZED)
    elif request.method == 'GET':
        serializer = SuggestedWorkoutSerializer(
            detailed_suggested_workout, context={'request': request})
        if(request.user.id != detailed_suggested_workout.coach.id and request.user.id != detailed_suggested_workout.athlete.id):
            return Response({"messages": response_messages["must_be_coach_or_athlete_info"]}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        if(request.user.id != detailed_suggested_workout.coach.id and request.user.id != detailed_suggested_workout.athlete.id):
            return Response({"messages": response_messages["must_be_coach_or_athlete_action"]}, status=status.HTTP_401_UNAUTHORIZED)
        SuggestedWorkout.delete(detailed_suggested_workout)
        return Response({"message": response_messages["suggested_workout_deleted"]}, status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        if(request.user.id != detailed_suggested_workout.coach.id and request.user.id != detailed_suggested_workout.athlete.id):
            return Response({"messages": response_messages["must_be_coach_or_athlete_action"]}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = SuggestedWorkoutSerializer(
            detailed_suggested_workout, data=request.data)
        if(serializer.is_valid()):
            serializer.update(instance=SuggestedWorkout.objects.get(id=pk),
                              validated_data=serializer.validated_data)
            return Response({"message": response_messages["suggested_workout_updated"]}, status=status.HTTP_200_OK)
        return Response({"message": response_messages["something_went_wrong"], "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
