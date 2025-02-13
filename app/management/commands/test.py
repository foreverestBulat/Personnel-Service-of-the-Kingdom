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
        subject = Subject.objects.get(id=3)
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
            
        print(data)
        
        
        # king = King.objects.get(id=1)
        # print(king.subjects.all())
        # a = ['1', '2', '3']
        # b = list(map(int, a))
        # print(b)
        
        # test = CandidateTestTrial.objects.filter(kingdom_code='LANNISTER').first()
        # print(test.questions.all())
        # for question in test.questions.all():
        #     print(question.text)
        
        