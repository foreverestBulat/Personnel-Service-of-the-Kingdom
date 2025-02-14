import logging
import os
import pandas as pd
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.core.exceptions import ValidationError

from django.utils.decorators import method_decorator 

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.decorators import role_required
from app.forms import (
    AuthForm,
    RegistrationForm,
    TestForm
)
from app.models import CandidateTestTrial, King, Subject, TestCase, User


logger = logging.getLogger('custom_logger')

class MainView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main.html'
    
    def get(self, request: HttpRequest):
        data = {}
        if request.user.is_authenticated:
            if request.user.king is not None:
                data = {
                    'tested_subjects': Subject.objects.filter(kingdom=request.user.king.kingdom, status=Subject.Status.NOT_ENROLLED)
                }
        return Response(data)


@login_required
def logout_user(request):
    logger.info(f'Пользователь {request.user.username} разлогинился.')
    logout(request)
    return redirect('main')


class RegView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'reg.html'
    
    def get(self, request):
        form = RegistrationForm()
        return Response({
            'form': form,
        })
        
    def post(self, request):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            king = None
            subject = None
            
            if form.cleaned_data['role'] == 'King':
                king = King(
                    name=form.cleaned_data['username'],
                    kingdom=form.cleaned_data['kingdom']
                )
                king.save()
            else:
                subject = Subject(
                    name=form.cleaned_data['username'],
                    kingdom=form.cleaned_data['kingdom'],
                    age=form.cleaned_data['age'],
                    email=form.cleaned_data['email']
                )
                subject.save()
            
            user = User(
                email=form.cleaned_data["email"],
                username=form.cleaned_data["username"],
                king=king,
                subject=subject
            )
            user.set_password(form.cleaned_data["password1"])
            user.save()
            
            logger.info(f'Зарегистрировался новый пользователь: {user.username}')
            return redirect('auth')
            
        return Response({
            'form': form,
        })


class AuthView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'auth.html'
    
    def get(self, request):
        form = AuthForm()
        return Response({
            'form': form
        })
    
    def post(self, request):
        form = AuthForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
                logger.info(f'Пользователь {request.user.username} авторизовался.')
                return redirect('main')
        
        return Response({
            'form': form
        })
        
        
class TestView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'test.html'
    
    @method_decorator(role_required('subject'))
    def get(self, request: HttpRequest):
            data = {}
            if request.user.subject.test_case is None:
                test_trial = CandidateTestTrial.objects.filter(kingdom_code=request.user.subject.kingdom.code).first()
                if test_trial is None:
                    data = {'test_created': False}
                else:
                    request.user.subject.test_case = TestCase.objects.create(
                        test=test_trial,
                        status=TestCase.Status.NOT_SOLVED
                    )
                    request.user.subject.save()
                    data = {
                        'test_created': True,
                        'form': TestForm(test_trial.questions.all())
                    }
            elif request.user.subject.test_case.status == TestCase.Status.NOT_SOLVED:
                test_trial = CandidateTestTrial.objects.filter(kingdom_code=request.user.subject.kingdom.code).first()
                data = {
                    'test_created': True,
                    'form': TestForm(test_trial.questions.all())
                }
            return Response(data)
    
    @method_decorator(role_required('subject'))
    def post(self, request):
        test_trial = CandidateTestTrial.objects.filter(kingdom_code=request.user.subject.kingdom.code).first()
        form = TestForm(test_trial.questions.all(), request.POST)
        if form.is_valid():
            answers = []
            for key, value in form.cleaned_data.items():
                answers.append({
                    'question_id': int(key),
                    'selected_answers': list(map(int, value))
                })
            request.user.subject.test_case.answers = {
                'selected_answers': answers
            }
            request.user.subject.test_case.status = TestCase.Status.SOLVED
            request.user.subject.test_case.save()
            logger.info(f'Пользователь {request.user.username} прошел тест')
            
        return redirect('main')

        
class CandidateResultView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'test_result.html'
    
    @method_decorator(role_required('king'))
    def get(self, request, id):
        subject = Subject.objects.get(id=id)
        data = {'subject': subject, 'test': []}
        for selected_answers, question in zip(subject.test_case.answers.get('selected_answers'), subject.test_case.test.questions.all()):
            answers = question.answer_options.get('answer_options')
            question_data = []
            correct_answers = question.answer_options.get('correct_answers')
            for key, value in answers.items():
                is_correct = False
                if int(key) in correct_answers:
                    is_correct = True
                question_data.append({
                    'number': key,
                    'answer': value,
                    'is_correct': is_correct
                })
            if len(question_data) > 0:
                data['test'].append({
                    'question_id': question.id,
                    'text': question.text,
                    'options': question_data,
                    'selected_answers': selected_answers['selected_answers']
                })
        return Response(data)
    
    
class AddCandidateForKing(APIView):
    @method_decorator(role_required('king'))
    def get(self, request, id):
        # if request.user.king.subjects.count() + 1 > 3:
        #     raise ValidationError(f"Количество подданных не может быть больше {self.MAX_SUBJECTS}")
        
        subject = Subject.objects.get(id=id)
        subject.status = Subject.Status.ENROLLED
        subject.king = request.user.king
        # request.user.king.subjects.add(subject)
        # request.user.king.save()
        subject.save()
        logger.info(f'Пользователь {request.user.username} зачислил в подданные Короля пользователя {subject.name}.')
        return redirect('main')
    

class DeleteCandidateForKing(APIView):
    @method_decorator(role_required('king'))
    def get(self, request, id):
        subject = Subject.objects.get(id=id)
        subject.status = Subject.Status.NOT_ENROLLED
        subject.king = None
        subject.save()
        logger.info(f'Пользователь {request.user.username} удалил из подданных Короля пользователя {subject.name}.')
        return redirect('main')
    

def export_logs_to_excel(request):
    log_file = "logs/django_actions.log"  # Путь к файлу логов

    if not os.path.exists(log_file):
        return HttpResponse("Файл логов не найден", status=404)

    # Читаем логи
    with open(log_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Парсим логи
    data = []
    for line in lines:
        parts = line.strip().split(" ", 3)  # Разбиваем строку на части
        if len(parts) < 4:
            continue
        level, timestamp, module, message = parts
        data.append({"Level": level, "Timestamp": timestamp, "Module": module, "Message": message})

    df = pd.DataFrame(data)

    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="logs.xlsx"'

    with pd.ExcelWriter(response, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Logs", index=False)

    return response
