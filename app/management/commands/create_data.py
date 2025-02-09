from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from app.models import (
    Kingdom,
    Subject,
    King,
    CandidateTestTrial,
    Question
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        (kingdom, created) = Kingdom.objects.get_or_create(
            name='Королевство Севера (дом старков)',
            code='STARK'
        )
        (king, created) = King.objects.get_or_create(
            name='Эддард Старк',
            kingdom=kingdom,
        )
        
        (subject, created) = Subject.objects.get_or_create(
            name='Джон Сноу',
            email='john_snow@gmail.com',
            age=18,
            kingdom=kingdom,
        )
        (subject, created) = Subject.objects.get_or_create(
            name='Робб Старк',
            email='robb_stark@gmail.com',
            age=18,
            kingdom=kingdom,
        )
        
        king.subjects.add(subject)
        
        (test, created) = CandidateTestTrial.objects.get_or_create(
            name_test='Рыцарь Короля',
            kingdom_code=kingdom.code,
            kingdom=kingdom
        )
        (question, created) = Question.objects.get_or_create(
            text='Кто ваш король?',
            answer_options={
                'answer_options': {
                    1: 'Эддард Старк',
                    2: 'Джон Сноу',
                    3: 'Рабберт Баратеон',
                    4: 'Дейенерис Таргариен'
                },
                'correct_answers': [1]
            }
        )
        test.questions.add(question)
        (question, created) = Question.objects.get_or_create(
            text='За что ты ненавидешь Джоффри Баратеона?',
            answer_options={
                'answer_options': {
                    1: 'Отсутствие сочувствия и эмпатии',
                    2: 'Неуравновешенность',
                    3: 'Некомпетентность как правитель',
                    4: 'Трусость',
                    5: 'Садизм и жестокость'
                },
                'correct_answers': [1, 2, 3, 4, 5]
            }
        )
        test.questions.add(question)
        
        
        
        
        
        (kingdom, created) = Kingdom.objects.get_or_create(
            name='Королевство Гор и Долины (дом Арренов)',
            code='ARREN'
        )
        (king, created) = King.objects.get_or_create(
            name='Роберт Аррен',
            kingdom=kingdom
        )
        
        (kingdom, created) = Kingdom.objects.get_or_create(
            name='Железные острова (дом Хоаров)',
            code='HOAR'
        )
        (king, created) = King.objects.get_or_create(
            name='Харрен Хоар',
            kingdom=kingdom
        )
        
        (kingdom, created) = Kingdom.objects.get_or_create(
            name = 'Королевство Утёса (дом Ланнистеров)',
            code = 'LANNISTER'
        )
        (king, created) = King.objects.get_or_create(
            name='Тайвин Ланнистер',
            kingdom=kingdom
        )
        
        (kingdom, created) = Kingdom.objects.get_or_create(
            name = 'Штормовые земли (дом Дюррандов)',
            code = 'DURRAND'
        )
        (king, created) = King.objects.get_or_create(
            name='Дюрран Богоборец',
            kingdom=kingdom
        )
        
        (kingdom, created) = Kingdom.objects.get_or_create(
            name = 'Королевство Простора (дом Гарденеров)',
            code = 'GARDENER'
        )
        (king, created) = King.objects.get_or_create(
            name='Гарт Гарденер',
            kingdom=kingdom
        )
        
        (kingdom, created) = Kingdom.objects.get_or_create(
            name = 'Дорн (дом Мартеллов)',
            code = 'MARTELL'
        )
        (king, created) = King.objects.get_or_create(
            name='Доран Мартелл',
            kingdom=kingdom
        )