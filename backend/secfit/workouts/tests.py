from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from workouts.permissions import IsOwner, IsOwnerOfWorkout, IsCoachAndVisibleToCoach, IsCoachOfWorkoutAndVisibleToCoach, IsPublic, IsWorkoutPublic, IsReadOnly
from django.utils import timezone
from workouts.models import Workout, ExerciseInstance, Exercise
from rest_framework.test import APIRequestFactory, APITestCase


class WorkoutPermissionsTestCases(TestCase):
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
        # Creating an object that has a workout instance. This object is an ExerciseInstance whichi needs an Exercise
        self.exercise = Exercise.objects.create(
            name="dummy_exercise", description='Dummy description', unit='rep')
        self.exercise.save()
        self.exercise_instance = ExerciseInstance.objects.create(
            workout=self.workout, suggested_workout=None, exercise=self.exercise, sets=2, number=2)
        self.exercise_instance.save()
        self.request = self.factory.delete('/')

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
        # Now check for the case where there exist no workout for the id
        fake_request_data_no_workout = {}
        self.request.data = fake_request_data_no_workout
        self.assertFalse(permission_class.has_permission(
            self, request=self.request, view=None))

        # Should always return True for has_permission when the method is not a POST
        self.request.method = 'GET'
        self.assertTrue(permission_class.has_permission(
            self, request=self.request, view=None))
        # Check for the case where request.user is owner
        self.request.user = self.owner
        self.assertTrue(permission_class.has_permission(
            self, request=self.request, view=None))
        """
        Test has_object_permission
        """
        self.assertTrue(permission_class.has_object_permission(
            self, self.request, view=None, obj=self.exercise_instance))
        # Test for where the requested user is not the workout for the exercise instance
        self.request.user = self.user
        self.assertFalse(permission_class.has_object_permission(
            self, self.request, view=None, obj=self.exercise_instance))

    def test_is_coach_and_visible_to_coach(self):
        # Make a coach to the owner of workout defined in setUp
        self.coach_of_owner = get_user_model()(id=3, username='owner', email='email@owner.com', phone_number='98154654',
                                               country='England', city='London', street_address='...'
                                               )
        self.coach_of_owner.save()
        self.owner.coach = self.coach_of_owner
        self.owner.save()
        print(self.owner.coach)
        self.request.user = self.coach_of_owner
        permission_class = IsCoachAndVisibleToCoach
        self.assertTrue(IsCoachAndVisibleToCoach.has_object_permission(
            self, request=self.request, view=None, obj=self.workout))
        # Changing the visibility to coach to see if it still works
        self.workout.visibility = 'CO'
        self.workout.save()
        self.assertTrue(IsCoachAndVisibleToCoach.has_object_permission(
            self, request=self.request, view=None, obj=self.workout))
        # Changing request.user to someoner who is not the owner's coach
        self.request.user = self.user
        self.assertFalse(IsCoachAndVisibleToCoach.has_object_permission(
            self, request=self.request, view=None, obj=self.workout))
        # Check if you get the same result when visibility is set to public and requested user is still not coach of owner
        self.workout.visibility = 'PU'
        self.workout.save()
        self.assertFalse(self.assertFalse(IsCoachAndVisibleToCoach.has_object_permission(
            self, request=self.request, view=None, obj=self.workout)))
        # Now, check if the function returns false when visibility is set to private
        # for both cases where requested user is coach or not coach of owner
        self.workout.visibility = 'PR'
        self.workout.save()
        self.assertFalse(IsCoachAndVisibleToCoach.has_object_permission(
            self, request=self.request,
            view=None, obj=self.workout))
        # Changing requested user back to coach. Should still return false
        self.request.user = self.coach_of_owner
        self.assertFalse(IsCoachAndVisibleToCoach.has_object_permission(self, request=self.request,
                                                                        view=None, obj=self.workout))

        # This test fails. Had to fix the fault in the permission class

    def is_coach_of_workout_and_visible_to_coach(self):
        """
        Testing for the exercise_instance instead of the workout directly
        """
        permission_class = IsCoachOfWorkoutAndVisibleToCoach
        # Make a coach to the owner of workout defined in setUp
        self.coach_of_owner = get_user_model()(id=3, username='owner', email='email@owner.com', phone_number='98154654',
                                               country='England', city='London', street_address='...'
                                               )
        self.coach_of_owner.save()
        self.owner.coach = self.coach_of_owner
        self.owner.save()
        # Check if false when requesting user is not the owner's coach
        self.request.user = self.user
        self.assertFalse(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=self.exercise_instance))

        self.request.user = self.coach_of_owner
        self.assertTrue(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=self.exercise_instance))
        # Changing the visibility to coach to see if it still works
        self.workout.visibility = 'CO'
        self.workout.save()
        self.assertTrue(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=self.exercise_instance))
        # Changing request.user to someoner who is not the owner's coach
        self.request.user = self.user
        self.assertFalse(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=self.exercise_instance))
        # Check if you get the same result when visibility is set to public and requested user is still not coach of owner
        self.workout.visibility = 'PU'
        self.workout.save()
        self.assertFalse(self.assertFalse(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=self.exercise_instance)))
        # Now, check if the function returns false when visibility is set to private
        # for both cases where requested user is coach or not coach of owner
        self.workout.visibility = 'PR'
        self.workout.save()
        self.assertFalse(permission_class.has_object_permission(
            self, request=self.request,
            view=None, obj=self.exercise_instance))
        # Changing requested user back to coach. Should still return false
        self.request.user = self.coach_of_owner
        self.assertFalse(permission_class.has_object_permission(self, request=self.request,
                                                                view=None, obj=self.exercise_instance))

        # This test fails. Had to fix the fault in the permission class
    def test_is_public(self):
        permission_class = IsPublic
        self.workout.visibility = 'PU'
        self.assertTrue(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=self.workout))
        """
        Other visibility levels should return false 
        """
        self.workout.visibility = 'CO'
        self.assertFalse(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=self.workout))
        self.workout.visibility = 'PR'
        self.assertFalse(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=self.workout))

    def test_is_workout_public(self):
        permission_class = IsWorkoutPublic
        self.workout.visibility = 'PU'
        self.assertTrue(permission_class.has_object_permission(
            self, request=None, view=None, obj=self.exercise_instance))
        self.workout.visibility = 'CO'
        self.assertFalse(permission_class.has_object_permission(
            self, request=None, view=None, obj=self.exercise_instance))
        self.workout.visibility = 'PR'
        self.assertFalse(permission_class.has_object_permission(
            self, request=None, view=None, obj=self.exercise_instance))

    def test_is_read_only(self):
        permission_class = IsReadOnly
        """
        Testing if false when unsafe methods are provided
        """
        self.request.method = 'POST'
        self.assertFalse(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=None))
        self.request.method = 'PUT'
        self.assertFalse(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=None))
        self.request.method = 'DELETE'
        self.assertFalse(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=None))
        """
        Testing if safe methods return true
        """
        self.request.method = 'HEAD'
        self.assertTrue(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=None))

        self.request.method = 'GET'
        self.assertTrue(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=None))

        self.request.method = 'OPTIONS'
        self.assertTrue(permission_class.has_object_permission(
            self, request=self.request, view=None, obj=None))
