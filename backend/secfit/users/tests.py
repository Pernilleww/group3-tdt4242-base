from django.contrib.auth import get_user_model
# from django.test import TestCase
from users.serializers import UserSerializer
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.request import Request
from random import choice
from string import ascii_uppercase


class UserSerializerTestCase(APITestCase):
    # Set up test instance of a user and serialized data of that user
    def setUp(self):
        self.user_attributes = {
            "id": 1,
            "email": "fake@email.com",
            "username": "fake_user",
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

        self.serializer_data = {
            "id": self.user_attributes["id"],
            "email": self.user_attributes["email"],
            "username": self.user_attributes["username"],
            "password": self.user_attributes["phone_number"],
            "password1": self.user_attributes["country"],
            "athletes": [],
            "phone_number": self.user_attributes["phone_number"],
            "country": self.user_attributes["country"],
            "city": self.user_attributes["city"],
            "street_address": self.user_attributes["street_address"],
            "coach": "",
            "workouts": [],
            "coach_files": [],
            "athlete_files": [],
        }

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

    def test_corresponding_id_field(self):
        serialized_data = self.serialized_user.data
        print(serialized_data)
        self.assertEqual(serialized_data[
            "id"
        ], self.user_attributes['id'])

    def test_corresponding_email_field(self):
        serialized_data = self.serialized_user.data
        self.assertEqual(serialized_data[
            "email"
        ], self.user_attributes['email'])

    def test_corresponding_username_field(self):
        serialized_data = self.serialized_user.data
        self.assertEqual(serialized_data[
            "username"
        ], self.user_attributes['username'])

    def test_corresponding_phone_number_field(self):
        serialized_data = self.serialized_user.data
        self.assertEqual(serialized_data[
            "phone_number"
        ], self.user_attributes['phone_number'])

    def test_corresponding_country_field(self):
        serialized_data = self.serialized_user.data
        self.assertEqual(serialized_data[
            "country"
        ], self.user_attributes['country'])

    def test_corresponding_city_field(self):
        serialized_data = self.serialized_user.data
        self.assertEqual(serialized_data[
            "country"
        ], self.user_attributes['country'])

    def test_corresponding_street_address_field(self):
        serialized_data = self.serialized_user.data
        self.assertEqual(serialized_data[
            "street_address"
        ], self.user_attributes['street_address'])

    # Teste om validering gjøres riktig for datatypene til username
    def test_invalid_username(self):
        self.serializer_data["username"] = '< > tralalala < / >'
        serializer_with_invalid_username = UserSerializer(
            data=self.serializer_data)
        print(serializer_with_invalid_username)
        self.assertFalse(serializer_with_invalid_username.is_valid())
        self.assertEqual(
            set(serializer_with_invalid_username.errors.keys()), set(['username']))

    def test_max_length_phone_number(self):
        # Generating random string of a length above valid max_length
        self.serializer_data["phone_number"] = ''.join(
            choice(ascii_uppercase) for i in range(60))
        serializer_with_invalid_phone_number = UserSerializer(
            data=self.serializer_data)
        self.assertFalse(serializer_with_invalid_phone_number)
    # Må lage test som sjekker om coach-athlete relasjonen opprettholdes
