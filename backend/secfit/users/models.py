from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    coach = models.ForeignKey(
        "self", on_delete=models.CASCADE, related_name="athletes", blank=True, null=True
    )
    phone_number = models.TextField(max_length=50, blank=True)
    country = models.TextField(max_length=50, blank=True)
    city = models.TextField(max_length=50, blank=True)
    street_address = models.TextField(max_length=50, blank=True)
    

def athlete_directory_path(instance, filename):
    return f"users/{instance.athlete.id}/{filename}"


class AthleteFile(models.Model):
    athlete = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="coach_files"
    )
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="athlete_files"
    )
    file = models.FileField(upload_to=athlete_directory_path)


class Offer(models.Model):
    owner = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="sent_offers"
    )
    recipient = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name="received_offers"
    )

    ACCEPTED = "a"
    PENDING = "p"
    DECLINED = "d"
    STATUS_CHOICES = (
        (ACCEPTED, "Accepted"),
        (PENDING, "Pending"),
        (DECLINED, "Declined"),
    )

    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default=PENDING)
    timestamp = models.DateTimeField(auto_now_add=True)
