import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.utils.translation import gettext_lazy as _ 

from app.models import Subject, Notification, User

logger = logging.getLogger('custom_logger')

@receiver(post_save, sender=Subject)
def send_enrollment_notification(sender, instance, created, **kwargs):
    if instance.status == Subject.Status.ENROLLED:

        message = _("Вы были зачислены в королевство.") 
        user = User.objects.get(email=instance.email)
        Notification.objects.create(user=user, message=message)
        
        # send_mail(
        #     'Зачисление в королевство',
        #     message,
        #     'from@example.com',
        #     [instance.email],
        #     fail_silently=False,
        # )
        
        logger.info(f'Пользователю {user.username} отправлено уведомление.')