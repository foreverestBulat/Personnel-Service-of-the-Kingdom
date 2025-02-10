from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator 

from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from app.forms import (
    AuthForm,
    RegistrationForm
)
from app.models import King, Subject, User


class MainView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'main.html'
    
    def get(self, request):
        return Response()


def logout_user(request):
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
                    age=18,
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
        print(request.POST)
        form = AuthForm(request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(request, username=username, password=password)
            if user is None:
                form.add_error(None, "Введены неверные данные")
            else:
                login(request, user)
        
        return Response({
            'form': form
        })