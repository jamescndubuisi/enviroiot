from django import forms
from django.contrib.auth.forms import UserCreationForm
from restiot import models
from datetime import date


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password"}))


class CreateUser(UserCreationForm):
    email = forms.CharField(label="Email ", widget=forms.EmailInput(attrs={"class": "form-control", "id": "username"}))
    password1 = forms.CharField(label="Password ",
                                widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password"}))
    password2 = forms.CharField(label="Confirm Password ",
                                widget=forms.PasswordInput(attrs={"class": "form-control", "id": "password"}))

    class Meta:
        model = models.User
        fields = ("email", "password1", "password2")
