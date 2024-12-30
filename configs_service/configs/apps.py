from django.apps import AppConfig


class ConfigsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'configs'

    # регистрация OpenAPI схемы для кастомной аутентификации
    def ready(self):
        import configs.schema
