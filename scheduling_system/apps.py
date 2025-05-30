from django.apps import AppConfig


class SchedulingSystemConfig(AppConfig):
    name = 'scheduling_system'

    def ready(self):
        import scheduling_system.signals
