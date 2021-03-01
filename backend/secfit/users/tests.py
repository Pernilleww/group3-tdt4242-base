from rest_framework.test import APITestCase


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
        self.test_user = User.create(**user_attributes)
        self.test_user.set_password("fake")
        self.serialized_user = UserSerializer(test_user)

    def test_contains_expected_fields(self):
        serialized_data = self.serialized_user.data
        self.assertEqual(set(data.keys()), set([{
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
        }]))

    def tearDown(self):
        return super().tearDown()
