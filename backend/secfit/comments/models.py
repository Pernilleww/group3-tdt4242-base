from django.db import models


from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.db import models
from django.contrib.auth import get_user_model
from workouts.models import Workout
from django.utils import timezone

class Comment(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="comments"
    )
    workout = models.ForeignKey(
        Workout, on_delete=models.CASCADE, related_name="comments"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-timestamp"]
