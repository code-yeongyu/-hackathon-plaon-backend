from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

import drf_yasg.openapi as openapi

from custom_profile.models import Profile


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        parameters = [
            openapi.Parameter('username',
                              openapi.IN_QUERY,
                              description="username",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('email',
                              openapi.IN_QUERY,
                              description="email",
                              type=openapi.FORMAT_EMAIL),
            openapi.Parameter('password1',
                              openapi.IN_QUERY,
                              description="password",
                              type=openapi.FORMAT_PASSWORD),
            openapi.Parameter('password2',
                              openapi.IN_QUERY,
                              description="password",
                              type=openapi.FORMAT_PASSWORD),
        ]