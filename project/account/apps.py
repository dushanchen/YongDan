from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        autodiscover_modules('api')