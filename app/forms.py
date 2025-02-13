from typing import List
from django import forms
from django.db import models

from app.models import (
    Kingdom,
    Question,
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
    age = forms.IntegerField()
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)

    kingdom = forms.ModelChoiceField(
        queryset=Kingdom.objects.all(),
        label="Выберите Королевство",
        empty_label="-----"
    )
    
    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data["age"] < 0:
            self.add_error("age", "Возраст не может быть отрицательным числом")
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
    

class TestForm(forms.Form):
    def __init__(self, questions, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.questions = questions
        
        for question in questions:
            if 'answer_options' in question.answer_options:
                answer_options = question.answer_options['answer_options']
                self.fields[f'{question.id}'] = forms.MultipleChoiceField(
                    choices=[(key, value) for key, value in answer_options.items()],
                    widget=forms.CheckboxSelectMultiple,
                    label=question.text,
                    required=True,
                )
            else:
                raise ValueError("Ключ 'answer_options' не найден в JSON")

    def clean(self):
        print(self.cleaned_data)
        for key, value in self.cleaned_data.items():
            if len(value) < 1:
                self.add_error(key, 'Не указан ответ.')