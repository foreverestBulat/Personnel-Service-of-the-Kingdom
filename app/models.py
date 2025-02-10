from django.db import models
from django.contrib.auth.models import AbstractUser, Permission, Group


class User(AbstractUser):
    king = models.ForeignKey(
        'King', 
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Король'
    )
    subject = models.ForeignKey(
        'Subject',
        null=True,
        on_delete=models.CASCADE,
        verbose_name='Подданный'
    )
    groups = models.ManyToManyField(
        Group, related_name="app_user_groups", verbose_name=""
    )
    subject_permissions = models.ManyToManyField(
        Permission, related_name="app_user_permissions"
    )
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return f'{'Король' if self.king is not None else ('Подданный' if self.subject is not None else 'Пользователь')}: {self.username}'


class Kingdom(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Наименование'
    )
    code = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        verbose_name='Уникальный код королевства'
    )
    
    class Meta:
        verbose_name = 'Королевство'
        verbose_name_plural = 'Королевства'
        
    def __str__(self):
        return self.code


class Subject(models.Model):
    name = models.CharField(
        max_length=255, 
        null=False, 
        verbose_name='Имя'
    )
    age = models.IntegerField(
        null=False, 
        verbose_name='Возраст'
    )
    email = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        verbose_name='Голубь (email)'
    )
    kingdom = models.ForeignKey(
        Kingdom, 
        null=True, 
        on_delete=models.CASCADE, 
        verbose_name='Королевство'
    )
    solved_test_case = models.ManyToManyField(
        'SolvedTestCase',
        verbose_name='Решенные тестовые испытания'
    )

    class Meta:
        verbose_name = 'Подданный'
        verbose_name_plural = 'Подданные'
        
    def __str__(self):
        return self.name


class SolvedTestCase(models.Model):
    class Status(models.TextChoices):
        ENROLLED = 'Enrolled', 'Зачислен'
        NOT_ENROLLED = 'Not enrolled', 'Не зачислен'
    
    answers = models.JSONField(
        null=False,
        verbose_name='Выбранные ответы'
    )
    solved_test = models.OneToOneField(
        'CandidateTestTrial',
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Решенное тестовое задание'
    )
    status = models.CharField(
        choices=Status.choices, 
        null=True,
        verbose_name='Статус зачисления'
    )

class King(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Имя'
    )
    kingdom = models.OneToOneField(
        Kingdom,
        on_delete=models.CASCADE,
        verbose_name='Королевство'
    )
    subjects = models.ManyToManyField(
        Subject,
        null=True,
        default=None,
        verbose_name='Подданные'
    )
    
    class Meta:
        verbose_name = 'Король'
        verbose_name_plural = 'Короли'


class Question(models.Model):
    text = models.TextField(
        null=False,
        verbose_name='Вопрос'
    )
    answer_options = models.JSONField(
        null=False,
        verbose_name='Варианты ответа'
    )
    
    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class CandidateTestTrial(models.Model):
    name_test = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Имя теста'
    )
    kingdom_code = models.CharField(
        max_length=255,
        null=False,
        unique=True,
        verbose_name='Уникальный код королевства'
    )
    kingdom = models.ForeignKey(
        Kingdom,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Королевство'
    )
    questions = models.ManyToManyField(
        'Question',
        related_name='questions',
        verbose_name='Список вопросов'
    )
    
    class Meta:
        verbose_name = 'Тестовое испытание кандидата'
        verbose_name_plural = 'Тестовые испытания кандидатов'