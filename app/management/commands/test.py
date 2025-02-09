from django.core.management.base import BaseCommand

from app.models import (
    Kingdom,
    Subject,
    King,
    CandidateTestTrial,
    Question
)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        king = King.objects.get(id=1)
        print(king.subjects.all())