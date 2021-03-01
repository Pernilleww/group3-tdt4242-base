from django.contrib.auth import get_user_model
# from django.test import TestCase
from users.serializers import UserSerializer
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.request import Request


class UserSerializerTestCase(APITestCase):
    # Set up test instance of a user and serialized data of that user
    def setUp(self):
        self.user_attributes = {
            "username": "fake_user",
            "email": "fake@email.com",
            "phone_number": "92345678",
            "country": "Norway",
            "city": "Trondheim",
            "street_address": "Lade Alle",
        }
        factory = APIRequestFactory()
        request = factory.get('/')
        self.test_user = get_user_model()(**self.user_attributes)
        self.test_user.set_password("fake")
        self.serialized_user = UserSerializer(
            self.test_user, context={'request': Request(request)})

    # Test that the serializer return the expecte fields for a given user instance
    def test_contains_expected_fields(self):
        serialized_data = self.serialized_user.data
        self.assertEqual(set(serialized_data.keys()), set([
            "url",
            "id",
            "email",
            "username",
            "athletes",
            "phone_number",
            "country",
            "city",
            "street_address",
            "coach",
            "workouts",
            "coach_files",
            "athlete_files",
        ]))
    # Testing if serialized data matched the retrieved instance in the database

    def test_corresponding_model_fields(self):
        serialized_data = self.serialized_user.data
        # print(serialized_data)
        print(self.)
        self.assertEqual(set(serialized_data['id', 'email', 'username', 'phone_number', 'country',
                                             'city', 'street_address', 'coach'
                                             ]), set(self.test_user.values()))
