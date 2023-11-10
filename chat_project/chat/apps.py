from django.apps import AppConfig


class ChatConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'chat'

    def ready(self):
        try:
            import chat.management  # Import the management commands

            from chat.remove_inactive_users import start_bgtask
            start_bgtask()
        except ImportError:
            pass

