from django.apps import AppConfig


class UniProfConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'uni_prof'

    # def ready(self):
    #     import uni_prof.signals
