from django.urls import path

from app.views import (
    logout_user,    
    MainView,
    RegView,
    AuthView
)

urlpatterns = [
    path('registration', RegView.as_view(), name='reg'),
    path('auth', AuthView.as_view(), name='auth'),
    path('main', MainView.as_view(), name='main'),
    path('logout', logout_user, name='logout')
    # path('logout', LogoutView.as_view(), name='logout')
]