from django.contrib import admin

# Register your models here.
from app.models import (
    User,
    Kingdom,
    Subject,
    King,
    Question,
    CandidateTestTrial,
    TestCase,
    Notification
)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'king_id', 'subject_id')
    search_fields = ('username', 'email')


@admin.register(Kingdom)
class KingdomAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'email', 'kingdom')
    list_filter = ('kingdom', 'age')
    search_fields = ('name', 'email')
    
    
@admin.register(King)
class KingAdmin(admin.ModelAdmin):
    list_display = ('name', 'kingdom')
    search_fields = ('name',)
    

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'answer_options')
    search_fields = ('text',)
    
    
@admin.register(CandidateTestTrial)
class CandidateTestTrialAdmin(admin.ModelAdmin):
    list_display = ('kingdom_code', 'kingdom')
    search_fields = ('kingdom_code',)
    
    
@admin.register(TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    list_display = ('answers', 'test', 'status')
    search_fields = ('id',)
    list_filter = ('status',)
    
    
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'read', 'created_at')
    search_fields = ('name', 'message')
    list_filter = ('read',)