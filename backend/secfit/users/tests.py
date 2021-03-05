from django.contrib.auth import get_user_model
# from django.test import TestCase
from users.serializers import UserSerializer
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.request import Request
from random import choice
from string import ascii_uppercase
from users.models import User


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
        self.test_user.set_password("password")
        self.serialized_user = UserSerializer(
            self.test_user, context={'request': Request(request)})

        self.serializer_data = {
            "id": self.user_attributes["id"],
            "email": self.user_attributes["email"],
            "username": self.user_attributes["username"],
            "password": 'password',
            "password1": 'password',
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
        self.new_serializer_data = {
            "email": 'email@fake.com',
            "username": 'faker',
            "athletes": [],
            "password": 'fuck_django',
            "password1": 'fuck_django',
            "phone_number": '12345678',
            "country": 'Norge',
            "city": 'Oslo',
            "street_address": 'Mora di',
            "workouts": [],
            "coach_files": [],
            "athlete_files": [], }

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
        self.assertFalse(serializer_with_invalid_username.is_valid())
        # Sjekker om det er username som er med i error meldingen
        self.assertEqual(
            set(serializer_with_invalid_username.errors.keys()), set(['username']))

    def test_max_length_phone_number(self):
        # Generating random string of a length above valid max_length
        self.serializer_data["phone_number"] = ''.join(
            choice(ascii_uppercase) for i in range(60))
        serializer_with_invalid_phone_number = UserSerializer(
            data=self.serializer_data)
        self.assertFalse(serializer_with_invalid_phone_number.is_valid())
        self.assertEqual(
            set(serializer_with_invalid_phone_number.errors.keys()), set(['phone_number']))
    # Teste at det går an å lage bruker

    def test_create_user(self):
        # Sjekker at jeg får serialisert til OrderedDict, kompleks datatype som kan bruker for å lage instans
        new_serializer = UserSerializer(data=self.new_serializer_data)
        self.assertTrue(new_serializer.is_valid())
        # Lage bruker
        new_serializer.save()
        # Sjekker at brukeren faktisk ble laget med brukernavner, 'faker'
        self.assertEquals(get_user_model().objects.get(
            username=self.new_serializer_data['username']).username, self.new_serializer_data['username'])
        # Sjekk at resten av feltene til instansen faktisk er lik de du definerte i serializer sin data
        self.assertEquals(get_user_model().objects.get(
            username=self.new_serializer_data['username']).email, self.new_serializer_data['email'])
        self.assertEquals(get_user_model().objects.get(
            username=self.new_serializer_data['username']).street_address, self.new_serializer_data['street_address'])
        self.assertEquals(get_user_model().objects.get(
            username=self.new_serializer_data['username']).phone_number, self.new_serializer_data['phone_number'])
        self.assertEquals(get_user_model().objects.get(
            username=self.new_serializer_data['username']).country, self.new_serializer_data['country'])
        self.assertEquals(get_user_model().objects.get(
            username=self.new_serializer_data['username']).city, self.new_serializer_data['city'])
        user_password = get_user_model().objects.get(username='faker').password
        # Sjekker om plaintekst passordet matcher med den krypterte i databasen
        self.assertTrue(self.new_serializer_data['password'], user_password)

    def test_validate_password(self):
        self.assertEquals(UserSerializer(self.new_serializer_data).validate_password(
            self.new_serializer_data['password']), self.new_serializer_data['password'])
        # TODO: Sjekke hva validate_password gjør og om jeg da kan legge dette til i testen
