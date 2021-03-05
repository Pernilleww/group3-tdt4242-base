from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from workouts.permissions import IsOwner
from django.utils import timezone
from workouts.models import Workout
from rest_framework.test import APIRequestFactory, APITestCase


class WorkoutTestCases(APITestCase):
    def setUp(self):
        self.owner = get_user_model()(id=1, username='bitch', email='email@email.com', phone_number='92134654',
                                      country='Norway', city='Paradise city', street_address='Hemmelig'
                                      )
        print(self.owner)
        print(self.owner.id)
        self.owner.save()
        self.factory = APIRequestFactory()
        self.workout = Workout.objects.create(id=2, name='Ballesnerkel', date=timezone.now(), notes='Hva vil du?',
                                              owner=self.owner, visibility='PU'
                                              )
        self.workout.save()

    def test_ownership_workout(self):
        self.request = self.factory.delete('/')
        self.request.user = self.owner
        permission = IsOwner.has_object_permission(
            self, request=self.request, view=None, obj=self.workout)
        self.assertTrue(permission)

    # # Is used for files and exercise instances
    # def test_is_owner_of_workout(self):
    #     # Faker post request
    #     fake_request_data = {"workout": }
    #     self.request.method ='POST'
    #     self.request.data =
