from django.contrib.auth import get_user_model, password_validation
# from django.test import TestCase
from users.serializers import UserSerializer
from rest_framework.test import APIRequestFactory, APITestCase
from rest_framework.request import Request
from random import choice
from string import ascii_uppercase
from users.models import User
from django import forms
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


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
        with self.assertRaises(serializers.ValidationError):
            UserSerializer(self.new_serializer_data).validate_password(
                'short')

    def test_valid_pasword(self):
        self.new_serializer_data['password'] = '12345678910'
        self.new_serializer_data['password1'] = '12345678910'
        self.data = {'password': '12345678910', 'password1': '12345678910'}
        user_ser = UserSerializer(instance=None, data=self.data)
        # Returns the password as the value
        self.assertEquals(user_ser.validate_password(
            '12345678910'), self.data['password'])
