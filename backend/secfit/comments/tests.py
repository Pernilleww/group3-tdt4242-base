from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient, APITestCase, force_authenticate
from django.urls import reverse
from workouts.models import Workout
from comments.models import Comment
from django.contrib.auth import get_user_model
from django.utils import timezone
from comments.serializers import CommentSerializer
from django.db.models import Q


class CommentTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.owner_of_workout = get_user_model()(id=1, username='athlete', email='athlete@email.com', phone_number='92134654',
                                                 country='Norway', city='Oslo', street_address='Grünerløkka'
                                                 )
        self.owner_of_workout.save()

        self.public_workout = Workout.objects.create(id=1, name="This is a public workout.",
                                                     date=timezone.now(), notes="Some notes..", owner=self.owner_of_workout, planned=False, visibility="PU")
        self.public_workout.save()

        self.private_workout = Workout.objects.create(id=2, name="This is a private workout.",
                                                      date=timezone.now(), notes="Some notes..", owner=self.owner_of_workout, planned=False, visibility="PR")
        self.private_workout.save()

        self.workout_visible_to_coach = Workout.objects.create(id=3, name="This is a workout visible to only coach.",
                                                               date=timezone.now(), notes="Some notes..", owner=self.owner_of_workout, planned=False, visibility="CO")
        self.workout_visible_to_coach.save()

        self.owner_of_comment = get_user_model()(id=2, username='commenter', email='comment@email.com', phone_number='92134654',
                                                 country='Norway', city='Trondheim', street_address='Lade'
                                                 )
        self.owner_of_comment.save()

        self.comment_public_workout = Comment.objects.create(
            owner=self.owner_of_comment, workout=self.public_workout, content="Comment on the public workout with id = 1.")
        self.comment_public_workout.save()

        self.comment_private_workout1 = Comment.objects.create(
            owner=self.owner_of_workout, workout=self.private_workout, content="Comment on the private workout with id = 2.")
        self.comment_private_workout1.save()

        self.comment_private_workout2 = Comment.objects.create(
            owner=self.owner_of_comment, workout=self.private_workout, content="New comment on the private workout with id = 2.")

        self.comment_private_workout2.save()

        self.comment_visible_to_coach = Comment.objects.create(
            owner=self.owner_of_comment, workout=self.workout_visible_to_coach, content="Comment on workout visible to coach.")

        self.comment_visible_to_coach.save()

    def test_comment_list(self):
        self.client.force_authenticate(self.owner_of_comment)
        response = self.client.get(
            reverse('comment-list'))
        request = self.factory.get(
            reverse('comment-list'))

        filtered_comment = Comment.objects.filter(
            Q(workout__visibility="PU")
            | Q(owner=self.owner_of_comment)
            | (
                Q(workout__visibility="CO")
                & Q(workout__owner__coach=self.owner_of_comment)
            )
            | Q(workout__owner=self.owner_of_comment)
        ).distinct()

        comment_serializer = CommentSerializer(
            filtered_comment, many=True, context={'request': request})
        self.assertEquals(response.data['results'], comment_serializer.data)
