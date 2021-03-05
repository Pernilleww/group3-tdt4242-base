from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class SuggestedWorkout(models.Model):
    # Visibility levels
    ACCEPTED = "a"
    PENDING = "p"
    DECLINED = "d"
    STATUS_CHOICES = (
        (ACCEPTED, "Accepted"),
        (PENDING, "Pending"),
        (DECLINED, "Declined"),
    )
    name = models.CharField(max_length=100)
    date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField()
    coach = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="owner")
    athlete = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="athlete")

    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.name
 