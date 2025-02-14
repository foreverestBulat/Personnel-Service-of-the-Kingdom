from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save
from django.dispatch import receiver
from app.models import Subject, King


@receiver(pre_save, sender=Subject)
def validate_add_subject_for_king(sender, instance, **kwargs):
    if instance.king is not None:
        if instance.king.subjects.all().count() > 2:
            instance.king = None
            instance.status = Subject.Status.NOT_ENROLLED
    