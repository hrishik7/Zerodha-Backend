from django.apps import AppConfig
from equity_data.get_data import start


class EquityDataConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equity_data'

    def ready(self):
        start()
