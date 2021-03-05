from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from workouts.permissions import IsOwner, IsOwnerOfWorkout
from django.utils import timezone
from workouts.models import Workout, ExerciseInstance, Exercise
from rest_framework.test import APIRequestFactory, APITestCase


class WorkoutTestCases(TestCase):
    def setUp(self):
        self.owner = get_user_model()(id=1, username='bitch', email='email@email.com', phone_number='92134654',
                                      country='Norway', city='Paradise city', street_address='Hemmelig'
                                      )
        self.owner.save()
        self.user = get_user_model()(id=2, username='balle', email='email@fake.com', phone_number='92134654',
                                     country='Norway', city='Hmm', street_address='Hemmelig'
                                     )
        self.user.save()
        self.factory = APIRequestFactory()
        self.workout = Workout.objects.create(id=1, name='Ballesnerkel', date=timezone.now(), notes='Hva vil du?',
                                              owner=self.owner, visibility='PU'
                                              )
        self.workout.save()

    def test_ownership_workout(self):
        self.request = self.factory.delete('/')
        self.request.user = self.owner
        permission = IsOwner.has_object_permission(
            self, request=self.request, view=None, obj=self.workout)
        self.assertTrue(permission)
        self.request.user = self.user
        self.assertFalse(IsOwner.has_object_permission(
            self, request=self.request, view=None, obj=self.workout))

    # Is used for files and exercise instances
    def test_is_owner_of_workout(self):
        # Make fake request
        self.request = self.factory.delete('/')
        # Fake post request
        fake_request_data = {
            "workout": "http://127.0.0.1:8000/api/workouts/1/"}
        # Fake method for request
        self.request.method = 'POST'
        # Fake data
        self.request.data = fake_request_data
        # Setting initialized user who is the owner for the workout which is going to be retrieved
        self.request.user = self.owner
        permission_class = IsOwnerOfWorkout
        # Check has permission is working
        self.assertTrue(permission_class.has_permission(
            self, request=self.request, view=None))
        # Check for a user who is not owner of workout
        self.request.user = self.user
        self.assertFalse(permission_class.has_permission(
            self, request=self.request, view=None))
        # Should always return True for has_permission
        self.request.method = 'GET'
        self.assertTrue(permission_class.has_permission(
            self, request=self.request, view=None))
        # Creating an object that has a workout instance. This object is an ExerciseInstance whichi needs an Exercise
        exercise = Exercise.objects.create(
            name="dummy_exercise", description='Dummy description', unit='rep')
        exercise.save()
        exercise_instance = ExerciseInstance.objects.create(
            workout=self.workout, suggested_workout=None, exercise=exercise, sets=2, number=2)
        exercise_instance.save()
        self.assertFalse(permission_class.has_object_permission(
            self, self.request, view=None, obj=exercise_instance))
        # Test for where the requested user is actually the owner of the workout for the exercise instance
        self.request.user = self.owner
        self.assertTrue(permission_class.has_object_permission(
            self, self.request, view=None, obj=exercise_instance))
