from apscheduler.schedulers.background import BackgroundScheduler
from django.apps import AppConfig
from django.core.management import call_command


def reset_score_data():
    call_command("reset_score")


def add_score_data():
    call_command("add_score_data")


def add_car_data():
    call_command("add_car_data")


class AtlasTraficAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "atlas_trafic_app"

    def ready(self):
        scheduler = BackgroundScheduler()
        scheduler.add_job(add_car_data, "interval", hours=1)
        scheduler.add_job(add_score_data, "interval", hours=3)
        scheduler.add_job(reset_score_data, "cron", hour=0, minute=0)
        scheduler.start()
