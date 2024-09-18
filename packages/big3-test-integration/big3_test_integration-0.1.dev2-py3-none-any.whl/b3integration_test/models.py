from enum import Enum

from django.db import models
from b3integrations.models import AbstractSettingsSingleton


class SettingsTestIntegration(AbstractSettingsSingleton):
    name_1 = models.CharField(max_length=1000, null=True, blank=True)
    name_2 = models.CharField(max_length=1000, null=True, blank=True)
    password = models.CharField(max_length=1000, null=True, blank=True)

    class Meta:
        verbose_name = 'Настройки'
        verbose_name_plural = 'Настройки'

    def __str__(self):
        return '<<App settings "b3integration_test">>'
