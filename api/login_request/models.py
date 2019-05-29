from django.conf import settings
from django.db import models

# Create your models here.

from api.core.utils.fitsenum import BaseEnum


class StatusChoice(BaseEnum):
    SNT = 'Sent'  # отправлена
    UC = 'Under consideration'  # На рассмотрении
    APT = 'Accept'  # Принята
    DCN = 'Decline'  # Отклонена


class LoginRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    message = models.TextField(verbose_name='Текст заявки')
    status = models.CharField(verbose_name='статус',
                              max_length=3,
                              choices=StatusChoice.get_choices(),
                              default=StatusChoice.SNT.name)
