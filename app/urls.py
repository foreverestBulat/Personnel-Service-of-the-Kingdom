from django.urls import path

from app.views import (
    AddCandidateForKing,
    CandidateResultView,
    DeleteCandidateForKing,
    NotificationsView,
    TestView,
    export_logs_to_excel,
    logout_user,    
    MainView,
    RegView,
    AuthView
)

urlpatterns = [
    path('registration', RegView.as_view(), name='reg'),
    path('auth', AuthView.as_view(), name='auth'),
    path('main', MainView.as_view(), name='main'),
    path('logout', logout_user, name='logout'),
    path('test', TestView.as_view(), name='test'),
    path('test/result/<int:id>', CandidateResultView.as_view(), name='test_result'),
    path('candidate/add/<int:id>', AddCandidateForKing.as_view(), name='add_candidate'),
    path('candidate/delete/<int:id>', DeleteCandidateForKing.as_view(), name='delete_candidate'),
    path('export-logs', export_logs_to_excel, name='export_logs'),
    path('notifications', NotificationsView.as_view(), name='notifications')
]