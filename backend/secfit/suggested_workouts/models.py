from django.db import models
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone


class SuggestedWorkout(models.Model):
    # Visibility levels
    PUBLIC = "PU"  # Visible to all authenticated users
    COACH = "CO"  # Visible only to owner and their coach
    PRIVATE = "PR"  # Visible only to owner
    VISIBILITY_CHOICES = [
        (PUBLIC, "Public"),
        (COACH, "Coach"),
        (PRIVATE, "Private"),
    ]  # Choices for visibility level

    name = models.CharField(max_length=100)
    date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField()
    visibility = models.CharField(
        max_length=2, choices=VISIBILITY_CHOICES, default=COACH
    )
    coach = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE, related_name="author")
    athlete = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="athlete")
    ACCEPTED = "a"
    PENDING = "p"
    DECLINED = "d"
    STATUS_CHOICES = (
        (ACCEPTED, "Accepted"),
        (PENDING, "Pending"),
        (DECLINED, "Declined"),
    )

    status = models.CharField(
        max_length=8, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return self.name
    """
    Helper function for setting the athlete. Will be called when
    request for the suggested workout is accepted by the Athlete
    """

    def add_athlete(self, athlete):
        self.athlete.add(athlete)


"""
Model for defining a request for a suggested workout to an Athlete.
The sender will be the coach initiating the request and the reciever will be the Athlete to whom the
coach request the suggested workout to.
Inspired by https://youtu.be/hyJO4mkdwuM
"""


class WorkoutRequest(models.Model):
    sender = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="sender"
    )

    reciever = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="reciever"
    )
    is_active = models.BooleanField(default=True, blank=True)

    def __str__(self):
        return self.sender.username

    def accept(self):
        is_active = False
        self.save()

        # Create a utility function for setting date to the suggested workout
    def set_date(self, date):
        # Retrieve the suggested workout by the sender of the request
        suggested_workout = SuggestedWorkout.get(author=self.sender)
        # Try to set the date
        suggested_workout.date = date

    def decline(self):
        suggested_workout = SuggestedWorkout.get(author=self.sender)
        # Delete the created workout if request declined
        suggested_workout.delete()
        is_active = False
        self.save()
