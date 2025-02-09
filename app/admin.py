from django.contrib import admin

# Register your models here.
from app.models import (
    Kingdom,
    Subject,
    King,
    CandidateTestTrial,
    Question
)


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
    