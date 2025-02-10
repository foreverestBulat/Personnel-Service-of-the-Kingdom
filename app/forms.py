from django import forms
from django.db import models

from app.models import (
    Kingdom,
    User
)


class RegistrationForm(forms.ModelForm):
    class Role(models.TextChoices):
        KING = 'King', 'Король'
        SUBJECT = 'Subject', 'Подданный'

    role = forms.ChoiceField(
        required=False,
        widget=forms.RadioSelect,
        choices=Role.choices,
    )
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    kingdom = forms.ModelChoiceField(
        queryset=Kingdom.objects.all(),
        label="Выберите Королевство",
        empty_label="-----"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["password1"] != cleaned_data["password2"]:
            self.add_error("password1", "Пароли не совпадают")
        if cleaned_data["role"] == "":
            self.add_error("role", "Вы не указали за кого вы регистрируетесь")
        return cleaned_data


    class Meta:
        model = User
        fields = ("email", "username")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)