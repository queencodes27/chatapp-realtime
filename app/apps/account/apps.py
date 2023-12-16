from django.apps import AppConfig


class AccountConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.account"
    label: str = "account"

    def ready(self) -> None:
        import apps.account.signals
