from django.test import TestCase
from django.urls import reverse
# from django.db import IntegrityError
from django.db import utils
from app.models import CandidateTestTrial, Question, Kingdom, King, Subject, User, TestCase as MyTestCase
from rest_framework.test import APITestCase
from rest_framework import status

class ViewTestCase(TestCase):
    def test_main_page(self):
        """
        Проверяем на доступность главной страницы
        """
        response = self.client.get('/api/main')
        self.assertEqual(response.status_code, 200)
        

class RegViewTest(APITestCase):
    def setUp(self):
        kingdom, created = Kingdom.objects.get_or_create(
            name='Королевство Тестов',
            code='TEST'
        )
        self.kingdom = kingdom
        self.url = reverse('reg')

    def test_post_king(self):
        """
        Проверяем регистрацию нового короля
        """
        data = {
            'role': ['King'],
            'username': ['TestKing'],
            'kingdom': [self.kingdom.id],
            'age': [20],
            'password1': ['testpassword'],
            'password2': ['testpassword']
        }
        
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        king = King.objects.get(name='TestKing')
        self.assertEqual(king.name, 'TestKing')
        self.assertEqual(king.kingdom, self.kingdom)
        
        user = User.objects.filter(username='TestKing').first()
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.king, king)

    def test_post_subject(self):
        """
        Проверяем регистрацию нового подданного
        """
        data = {
            'role': ['Subject'],
            'username': ['TestSubject'],
            'kingdom': [self.kingdom.id],
            'age': [25],
            'email': ['subject@example.com'],
            'password1': ['testpassword'],
            'password2': ['testpassword']
        }

        response = self.client.post(self.url, data)

        self.assertEqual(response.status_code, status.HTTP_302_FOUND)  # ожидание редиректа

        subject = Subject.objects.get(name='TestSubject')
        self.assertEqual(subject.name, 'TestSubject')
        self.assertEqual(subject.kingdom, self.kingdom)
        
        user = User.objects.get(username='TestSubject')
        self.assertTrue(user.check_password('testpassword'))
        self.assertEqual(user.subject, subject)
        
    def test_post_invalid_data(self):
        """
        Проверяем случай с некорректными данными
        """
        data = {
            'role': 'King',
            'username': 'TestKing',
            'kingdom': self.kingdom.id,
            'age': 20,
            'password1': 'testpassword',
            'password2': 'wrongpassword'  # Неправильный пароль
        }

        response = self.client.post(self.url, data)
        
        form = response.context['form']
        self.assertFalse(form.is_valid())
        

class AuthViewTests(TestCase):

    def setUp(self):
        """
        Создаем нового пользователя
        """
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.url = reverse('auth')

    def test_get_request_renders_auth_form(self):
        """
        Отправляем GET запрос на страницу авторизации
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')

    def test_post_request_with_valid_data(self):
        """
        Отправляем POST запрос с правильными данными
        Проверяем, что после авторизации происходит редирект на главную страницу
        """
        response = self.client.post(self.url, {'username': self.username, 'password': self.password})
        self.assertRedirects(response, reverse('main'))
    
    def test_post_request_with_invalid_data(self):
        """
        Отправляем POST запрос с неправильными данными
        Проверяем, что возвращается форма с ошибками
        """
        response = self.client.post(self.url, {'username': 'wronguser', 'password': 'wrongpassword'})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Введены неверные данные')
        
        
class TestViewTests(TestCase):

    def setUp(self):
        (kingdom, created) = Kingdom.objects.get_or_create(
            name='Королевство Севера (дом старков)',
            code='STARK'
        )
        (king, created) = King.objects.get_or_create(
            name='Эддард Старк',
            kingdom=kingdom,
        )
        (user, created) = User.objects.get_or_create(
            email='eddard@stark.com',
            username='Eddard Stark',
            king=king,
        )
        if created:
            user.set_password('passwd')
            user.save()
            
        self.user_king = user
            
        (subject, created) = Subject.objects.get_or_create(
            name='Джон Сноу',
            email='john_snow@gmail.com',
            age=18,
            kingdom=kingdom,
        )
        (user, created) = User.objects.get_or_create(
            email='john@snow.com',
            username='John Snow',
            subject=subject
        )
        if created:
            user.set_password('passwd')
            user.save()
            
        self.user_subject = user

        (test, created) = CandidateTestTrial.objects.get_or_create(
            name_test='Тест Короля',
            kingdom_code=kingdom.code,
            kingdom=kingdom
        )
        (question, created) = Question.objects.get_or_create(
            text='Кто ваш король?',
            answer_options={
                'answer_options': {
                    1: 'Эддард Старк',
                    2: 'Джон Сноу',
                    3: 'Роберт Баратеон',
                    4: 'Дейенерис Таргариен'
                },
                'correct_answers': [1]
            }
        )
        test.questions.add(question)
        (question_joffry, created) = Question.objects.get_or_create(
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
        test.questions.add(question_joffry)
        test.save()
        
        self.test_trial = test

        self.client.login(username='John Snow', password='passwd')
        self.url = reverse('test')

    def test_post_request_verifying_correctness_data(self):
        """
        Проверяем верно ли передались данные и изменился ли статус TestCase не решенного на решенный
        """
        test_case = MyTestCase.objects.create(
            status=MyTestCase.Status.NOT_SOLVED, 
            test=self.test_trial            
        )
        self.user_subject.subject.test_case = test_case
        self.user_subject.subject.save()
        
        form_data = {
            '1': ['1'],
            '2': ['1', '2', '3']
        }
        response = self.client.post(self.url, form_data)
        
        self.assertRedirects(response, reverse('main'))
        
        test_case.refresh_from_db()
        self.assertEqual(test_case.status, MyTestCase.Status.SOLVED)
        self.assertDictEqual(
            test_case.answers,
            {'selected_answers': [
                {'question_id': 1, 'selected_answers': [1]}, 
                {'question_id': 2, 'selected_answers': [1, 2, 3]}
            ]}
        )


class KingModelTests(TestCase):
    
    def setUp(self):
        (kingdom, created) = Kingdom.objects.get_or_create(
            name='Королевство Севера (дом старков)',
            code='STARK'
        )
        (king, created) = King.objects.get_or_create(
            name='Эддард Старк',
            kingdom=kingdom,
        )
        (user, created) = User.objects.get_or_create(
            email='eddard@stark.com',
            username='Eddard Stark',
            king=king,
        )
        if created:
            user.set_password('passwd')
            user.save()
        
        self.user_king = user    
        
        (subject, created) = Subject.objects.get_or_create(
            name='Джон Сноу',
            email='john_snow@gmail.com',
            age=18,
            kingdom=kingdom,
        )
        (user, created) = User.objects.get_or_create(
            email='john@snow.com',
            username='John Snow',
            subject=subject
        )
        if created:
            user.set_password('passwd')
            user.save()
        self.user_subject_1 = user
            
        (subject, created) = Subject.objects.get_or_create(
            name='Робб Старк',
            email='robb_stark@gmail.com',
            age=18,
            kingdom=kingdom,
        )
        (user, created) = User.objects.get_or_create(
            email='robb@stark.com',
            username='Robb Stark',
            subject=subject
        )
        if created:
            user.set_password('passwd')
            user.save()
        self.user_subject_2 = user
            
        (subject, created) = Subject.objects.get_or_create(
            name='Санса Старк',
            email='sansa_stark@gmail.com',
            age=18,
            kingdom=kingdom,
        )
        (user, created) = User.objects.get_or_create(
            email='sansa_stark@gmail.com',
            username='Sansa Stark',
            subject=subject
        )
        if created:
            user.set_password('passwd')
            user.save()
        self.user_subject_3 = user
            
        (subject, created) = Subject.objects.get_or_create(
            name='Санса Старк',
            email='joffry_b@gmail.com',
            age=18,
            kingdom=kingdom,
        )
        (user, created) = User.objects.get_or_create(
            email='joffry_b@gmail.com',
            username='Joffry Barateon',
            subject=subject
        )
        if created:
            user.set_password('passwd')
            user.save()
        self.user_subject_4 = user
            
    def test_add_more_than_3_subjects(self):    
        """
        Проверяем, что король может добавить не более трех подданных
        """
        self.user_king.king.subjects.add(self.user_subject_1.subject)
        self.user_king.king.subjects.add(self.user_subject_2.subject)
        self.user_king.king.subjects.add(self.user_subject_3.subject)

        with self.assertRaises(utils.InternalError):
            self.user_king.king.subjects.add(self.user_subject_4.subject)