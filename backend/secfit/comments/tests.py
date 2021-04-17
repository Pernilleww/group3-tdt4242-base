from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate
from django.urls import reverse
from workouts.models import Workout
from comments.models import Comment
from django.contrib.auth import get_user_model
from django.utils import timezone
from comments.serializers import CommentSerializer


class CommentTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.owner = get_user_model()(id=1, username='athlete', email='athlete@email.com', phone_number='92134654',
                                      country='Norway', city='Oslo', street_address='Grünerløkka'
                                      )
        self.owner.save()
        self.workout = Workout.objects.create(id=1, name="This is a workout.",
                                              date=timezone.now(), notes="Some notes..", owner=self.owner, planned=False, visibility="PU")
        self.workout.save()
        self.owner_of_comment = get_user_model()(id=2, username='commenter', email='comment@email.com', phone_number='92134654',
                                                 country='Norway', city='Trondheim', street_address='Lade'
                                                 )
        self.owner.save()
        self.comment1 = Comment.objects.create(
            owner=self.owner, workout=self.workout, content="This is the first comment for the workout with id=1.")
        self.comment1.save()
        self.comment2 = Comment.objects.create(
            owner=self.owner, workout=self.workout, content="This is the second comment for the workout with id=1.")
        self.comment2.save()
        self.second_workout = Workout.objects.create(id=2, name="This is a new workout.",
                                                     date=timezone.now(), notes="Some notes for the second workout..", owner=self.owner, planned=False, visibility="PR")
        self.second_workout.save()

    def test_comment_list(self):
        self.client.force_authenticate(self.owner)
        response = self.client.get(
            reverse('comment-list'))
        request = self.factory.get(
            reverse('comment-list'))

        filtered_comment = Comment.objects.all()
        comment_serializer = CommentSerializer(
            filtered_comment, many=True, context={'request': request})
        self.assertEquals(response.data['results'], comment_serializer.data)
