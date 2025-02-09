from django.db import models
from django.contrib.postgres.fields import ArrayField



class Kingdom(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Наименование'
    )
    code = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Уникальный код королевства'
    )
    
    class Meta:
        verbose_name = 'Королевство'
        verbose_name_plural = 'Королевства'


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
        null=False, 
        on_delete=models.CASCADE, 
        verbose_name='Королевство'
    )
    
    class Meta:
        verbose_name = 'Подданный'
        verbose_name_plural = 'Подданные'


class King(models.Model):
    name = models.CharField(
        max_length=255,
        null=False,
        verbose_name='Имя'
    )
    kingdom = models.ForeignKey(
        Kingdom,
        null=False,
        on_delete=models.CASCADE,
        verbose_name='Королевство'
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
    kingdom_code = models.CharField(
        max_length=255,
        null=False,
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