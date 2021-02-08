from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model


class CustomUserCreationForm(UserCreationForm):

    phone_number = forms.CharField(max_length=50)
    country = forms.CharField(max_length=50)
    city = forms.CharField(max_length=50)
    street_address = forms.CharField(max_length=50)


    class Meta(UserCreationForm):
        model = get_user_model()
        fields = ("username", "coach", "phone_number", "country", "city", "street_address")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "coach")
