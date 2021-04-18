import json
from django.test import TestCase
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate, APIClient
from django.contrib.auth import get_user_model
from suggested_workouts.models import SuggestedWorkout
from suggested_workouts.serializer import SuggestedWorkoutSerializer
from django.utils import timezone
from workouts.models import Exercise, ExerciseInstance
from workouts.serializers import ExerciseSerializer
from django.urls import reverse
from suggested_workouts.views import create_suggested_workouts, detailed_suggested_workouts
from rest_framework import status
from suggested_workouts.views import response_messages


"""
Integration testing for new feature: UC2
"""


"""
Testing each endpoints are functioning are functioning as expected. Also testing if
the serializer is able to successfully serialize an existing suggested_workout instance, create a
new intance and update an existing instance. The integration testing is based on test if views.py and
urls.py are actually integrated and communicates as expected, but also that the SuggestedWorkout model
functions as expected together with the serializer, meaning that we test wheter the serializer is able
to deserialize, serialize, updating and creating an instance of SuggestedWorkout.
"""


class SuggestedWorkoutTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.coach = get_user_model()(id=1, username='coach', email='coach@email.com', phone_number='92134654',
                                      country='Norway', city='Trondheim', street_address='Moholt studentby'
                                      )
        self.coach.save()
        self.athlete = get_user_model()(id=2, username='athlete', email='athlete@email.com', phone_number='92134654', coach=self.coach,
                                        country='Norway', city='Oslo', street_address='Grünerløkka'
                                        )
        self.athlete.save()
        self.not_coach_nor_athlete = get_user_model()(id=3, username='not_coach_nor_athlete', email='', phone_number='92134654',
                                                      country='Norway', city='Trondheim', street_address='Baker street'
                                                      )
        self.not_coach_nor_athlete.save()
        self.suggested_workout = SuggestedWorkout.objects.create(id=1, name='This is a suggested workout',
                                                                 date=timezone.now(), notes='Some notes', coach=self.coach, athlete=self.athlete, status='p')
        self.suggested_workout.save()
        self.not_existing_suggested_workout_pk = self.suggested_workout.id + 1

        self.exercise_type = Exercise.objects.create(
            id=1, name='Plank', description='Train your core yall', unit='reps')
        self.exercise_type.save()
        self.new_exercise_type = Exercise.objects.create(
            id=2, name='Plank', description='Train your core yall', unit='reps')

    def test_serializer(self):
        suggested_workout_ser = SuggestedWorkoutSerializer(
            self.suggested_workout)
        expected_serializer_data = {
            'id': 1,
            'athlete': self.athlete.id,
            'coach_username': self.coach.username,
            'name': 'This is a suggested workout',
            'notes': 'Some notes',
            'date': '2021-03-07T17:28:44.443551Z',
            'status': 'p',
            'coach': self.coach.id,
            'status': 'p',
            'suggested_exercise_instances': [],
            'suggested_workout_files': []
        }
        self.assertEquals(set(expected_serializer_data,),
                          set(suggested_workout_ser.data,))
        new_serializer_data = {
            'athlete': self.athlete.id,
            'name': 'A new suggested workout',
            'notes': 'This is new',
            'date': None,
            'status': 'p',
            'suggested_exercise_instances': [{
                'exercise': 'http://localhost:8000/api/exercises/1/',
                'sets': 10,
                'number': 3
            }],
            'suggested_workout_files': []
        }
        new_suggested_workout_serializer = SuggestedWorkoutSerializer(
            data=new_serializer_data)
        self.assertTrue(new_suggested_workout_serializer.is_valid())
        new_suggested_workout_serializer.create(validated_data=new_suggested_workout_serializer.validated_data,
                                                coach=self.coach)
        # Check if suggested workout with the id=2 got created
        self.assertEquals(SuggestedWorkout.objects.get(id=2).id, 2)
        # Check if exercise instance got created
        self.assertEquals(ExerciseInstance.objects.get(id=1).id, 1)
        # Testing rest of the fields corresponds to new_serializer_data
        self.assertEquals(SuggestedWorkout.objects.get(
            id=2).athlete, self.athlete)
        self.assertEquals(SuggestedWorkout.objects.get(
            id=2).name, new_serializer_data['name'])
        self.assertEquals(SuggestedWorkout.objects.get(
            id=2).notes, new_serializer_data['notes'])
        self.assertEquals(SuggestedWorkout.objects.get(
            id=2).date, new_serializer_data['date'])
        self.assertEquals(SuggestedWorkout.objects.get(
            id=2).status, new_serializer_data['status'])
        # Testing for update
        updated_data = {'name': 'Suggested workout got updated', 'status': 'a',
                        'suggested_exercise_instances': [{
                            'exercise': 'http://localhost:8000/api/exercises/2/',
                            'sets': 5,
                            'number': 5
                        }]
                        }

        updated_suggested_workout_serializer = SuggestedWorkoutSerializer(
            instance=SuggestedWorkout.objects.get(id=2), data=updated_data, partial=True)

        self.assertTrue(updated_suggested_workout_serializer.is_valid())
        updated_suggested_workout_serializer.update(
            instance=SuggestedWorkout.objects.get(id=2), validated_data=updated_suggested_workout_serializer.validated_data)
        self.assertEquals(SuggestedWorkout.objects.get(
            id=2).name, updated_data['name'])
        self.assertEquals(SuggestedWorkout.objects.get(
            id=2).status, updated_data['status'])
        self.assertEquals(ExerciseInstance.objects.get(
            id=1).exercise, self.new_exercise_type)

    """
    Test if a coach can create a workout for their athlete when valid payload is given
    """

    def test_create_valid_suggested_workout(self):
        self.client.force_authenticate(user=self.coach)
        self.valid_payload = {
            "athlete": self.athlete.id,
            "name": "Oppdatert",
            "notes": "Ble du oppdatert nå?",
            "date": None,
            "status": "a",
            "suggested_exercise_instances": [{
                "exercise": 'http://localhost:8000/api/exercises/1/',
                "sets": 3,
                "number": 10

            }],
            "suggested_workout_files": []
        }

        response = self.client.post(
            reverse('suggested_workouts_create'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data['message'], response_messages["suggested_workout_created"])

    """
    Test invalid payload leads to status code 400
    """

    def test_create_invalid_suggested_workout(self):
        self.client.force_authenticate(user=self.coach)
        self.invalid_payload = {
            "athlete": self.athlete.id,
            "name": 1243234,
            "notes": 4534623654,
            "date": None,
            "status": "a",
            "suggested_exercise_instances": [1],
            "suggested_workout_files": []
        }

        response = self.client.post(
            reverse('suggested_workouts_create'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         response_messages["something_went_wrong"])

    """
    Test unauthenticated user can not create a suggested workout
    """

    def test_unauthenticated_create_suggested_workout_access_denied(self):
        self.client.force_authenticate(user=None)
        self.valid_payload = {
            "athlete": self.athlete.id,
            "name": "This should not be published",
            "notes": "....",
            "date": None,
            "status": "a",
            "suggested_exercise_instances": [{
                "exercise": 'http://localhost:8000/api/exercises/1/',
                "sets": 3,
                "number": 10

            }],
            "suggested_workout_files": []
        }

        response = self.client.post(
            reverse('suggested_workouts_create'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'],
                         response_messages["error_not_your_athlete"])

    """
    Test that a user who is not a coach of self.athlete can create a suggested workout to the athlete
    """

    def test_unauthorized_create_suggested_workout_access_denied(self):
        self.client.force_authenticate(user=self.not_coach_nor_athlete)
        self.valid_payload = {
            "athlete": self.athlete.id,
            "name": "This should not be published",
            "notes": "....",
            "date": None,
            "status": "a",
            "suggested_exercise_instances": [{
                "exercise": 'http://localhost:8000/api/exercises/1/',
                "sets": 3,
                "number": 10

            }],
            "suggested_workout_files": []
        }

        response = self.client.post(
            reverse('suggested_workouts_create'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'],
                         response_messages["error_not_your_athlete"])

    """
    Test that a coach of a suggested workout is able to access the suggested workout
    """

    def test_authorized_as_coach_retrieve_single_suggested_workout(self):
        self.client.force_authenticate(user=self.coach)
        response = self.client.get(
            reverse('suggested-workout-detail', kwargs={'pk': self.suggested_workout.id}))
        serializer = SuggestedWorkoutSerializer(self.suggested_workout)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    """
    Test that athlete of a suggested workout can access the suggested workout
    """

    def test_authorized_as_athlete_retrieve_single_suggested_workout(self):
        self.client.force_authenticate(user=self.athlete)
        response = self.client.get(
            reverse('suggested-workout-detail', kwargs={'pk': self.suggested_workout.id}))
        serializer = SuggestedWorkoutSerializer(self.suggested_workout)
        self.assertEqual(response.data, serializer.data)

    """
    Test that unauthenticated user can not access a suggested workout
    """

    def test_unauthenticated__retrieve_single_workout_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(
            reverse('suggested-workout-detail', kwargs={'pk': self.suggested_workout.id}))
        serializer = SuggestedWorkoutSerializer(self.suggested_workout)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'],
                         response_messages["access_denied"])
    """
    Test that a user who is neither a coach nor an athlete of the suggested workout can access the suggested workout
    """

    def test_unauthorized_retrieve_single_workout_access_denied(self):
        self.client.force_authenticate(user=self.not_coach_nor_athlete)
        response = self.client.get(
            reverse('suggested-workout-detail', kwargs={'pk': self.suggested_workout.id}))
        serializer = SuggestedWorkoutSerializer(self.suggested_workout)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    """
    Test that a coach of the suggested workout can update it
    """

    def test_authorized_update_as_coach_suggested_workout(self):
        self.client.force_authenticate(user=self.coach)
        self.exercise_type.save()
        self.valid_payload = {"athlete": self.athlete.id,
                              "name": "Updated suggested workout",
                              "notes": "Did the update work?",
                              "date": None,
                              "status": "p",
                              "suggested_exercise_instances": [
                                  {
                                      "exercise": 'http://localhost:8000/api/exercises/1/',
                                      "sets": 5,
                                      "number": 10
                                  },
                                  {
                                      "exercise": 'http://localhost:8000/api/exercises/2/',
                                      "sets": 1,
                                      "number": 5
                                  }
                              ],
                              "suggested_workout_files": []
                              }
        response = self.client.put(
            reverse('suggested-workout-detail',
                    kwargs={'pk': self.suggested_workout.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         response_messages["suggested_workout_updated"])

    """
    Test that athlete of suggested workout can update it
    """

    def test_authorized_as_athlete_update_suggested_workout(self):
        self.client.force_authenticate(user=self.athlete)
        self.valid_payload = {"athlete": self.athlete.id,
                              "name": "Updated suggested workout",
                              "notes": "Did the update work?",
                              "date": None,
                              "status": "p",
                              "suggested_exercise_instances": [
                                  {
                                      "exercise": 'http://localhost:8000/api/exercises/1/',
                                      "sets": 5,
                                      "number": 10
                                  },
                                  {
                                      "exercise": 'http://localhost:8000/api/exercises/2/',
                                      "sets": 1,
                                      "number": 5
                                  }
                              ],
                              "suggested_workout_files": []
                              }
        response = self.client.put(
            reverse('suggested-workout-detail',
                    kwargs={'pk': self.suggested_workout.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'],
                         response_messages["suggested_workout_updated"])

    """
    Testing invalid payloads leads to status code 400
    """

    def test_invalid_update_suggested_workout(self):
        self.client.force_authenticate(user=self.athlete)
        self.invalid_payload = {"athlete": 'athlete',
                                "name": "Updated suggested workout",
                                "notes": ['INVALID DATASTRUCTURE'],
                                "date": 123,
                                "status": 10,
                                "suggested_exercise_instances": [
                                    {
                                        "exercise": 1,
                                        "sets": 5,
                                        "number": 10
                                    },
                                    {
                                        "exercise": 2,
                                        "sets": 1,
                                        "number": 5
                                    }
                                ],
                                "suggested_workout_files": []
                                }
        response = self.client.put(
            reverse('suggested-workout-detail',
                    kwargs={'pk': self.suggested_workout.id}),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'],
                         response_messages["something_went_wrong"])

    """
    Test unauthenticated user can not perform an update of a suggested workout
    """

    def test_unauthenticated_update_suggested_workout_access_denied(self):
        self.client.force_authenticate(user=None)
        self.valid_payload = {"athlete": self.athlete.id,
                              "name": "Updated suggested workout",
                              "notes": "Did the update work?",
                              "date": None,
                              "status": "p",
                              "suggested_exercise_instances": [
                                  {
                                      "exercise": 'http://localhost:8000/api/exercises/2/',
                                      "sets": 5,
                                      "number": 10
                                  }

                              ],
                              "suggested_workout_files": []
                              }
        response = self.client.put(
            reverse('suggested-workout-detail',
                    kwargs={'pk': self.suggested_workout.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'],
                         response_messages["access_denied"])
    """
    Test that a user who is neither a coach or an athlete of the suggested workut can perform an update of the suggested workout
    """

    def test_unauthorized_update_suggested_workout_access_denied(self):
        self.client.force_authenticate(user=self.not_coach_nor_athlete)
        self.valid_payload = {"athlete": self.athlete.id,
                              "name": "Updated suggested workout",
                              "notes": "Did the update work?",
                              "date": None,
                              "status": "p",
                              "suggested_exercise_instances": [
                                  {
                                      "exercise": 'http://localhost:8000/api/exercises/1/',
                                      "sets": 5,
                                      "number": 10
                                  },
                                  {
                                      "exercise": 'http://localhost:8000/api/exercises/1/',
                                      "sets": 1,
                                      "number": 5
                                  },
                                  {
                                      "exercise": 'http://localhost:8000/api/exercises/2/',
                                      "sets": 5,
                                      "number": 5
                                  }
                              ],
                              "suggested_workout_files": []
                              }
        response = self.client.put(
            reverse('suggested-workout-detail',
                    kwargs={'pk': self.suggested_workout.id}),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    """
    Test that a coach of the suggested workout can delete it
    """

    def test_authorized_as_coach_delete_suggested_workout(self):
        self.client.force_authenticate(user=self.coach)
        response = self.client.delete(
            reverse('suggested-workout-detail', kwargs={'pk': self.suggested_workout.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],
                         response_messages["suggested_workout_deleted"])

    """
    Test that an athlete of the suggested workout can delete it
    """

    def test_authorized_delete_as_athlete_suggested_workout(self):
        self.client.force_authenticate(user=self.athlete)
        response = self.client.delete(
            reverse('suggested-workout-detail', kwargs={'pk': self.suggested_workout.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'],
                         response_messages["suggested_workout_deleted"])

    """
    Test that an unauthenticated user can not delete a suggested workout
    """

    def test_unauthenticated_delete_access_denied(self):
        self.client.force_authenticate(user=None)
        response = self.client.delete(
            reverse('suggested-workout-detail', kwargs={'pk': self.suggested_workout.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['message'],
                         response_messages["access_denied"])

    """
    Test that a user who is neither a coach or an athlete of the suggested workout can delete it
    """

    def test_unauthorized_delete_access_denied(self):
        self.client.force_authenticate(user=self.not_coach_nor_athlete)
        response = self.client.delete(
            reverse('suggested-workout-detail', kwargs={'pk': self.suggested_workout.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_returned_404_not_found(self):
        response = self.client.delete(
            reverse('suggested-workout-detail', kwargs={'pk': self.not_existing_suggested_workout_pk}))
        self.assertEqual(response.status_code, 404)
