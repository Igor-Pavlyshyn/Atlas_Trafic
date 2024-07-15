from django.core.management.base import BaseCommand
from atlas_trafic_app.models import Safety
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Reset scores data after 5 minutes'

    def handle(self, *args, **kwargs):
        reset_time = datetime.now() + timedelta(minutes=5)
        while True:
            if datetime.now() >= reset_time:
                Safety.objects.update(
                    points=120,
                    accident_rate=0,
                    near_misses=0,
                    speeding=0,
                    traffic_violations=0,
                    pedestrian_incidents=0,
                    damaged_disabled_vehicle=0
                )
                print("Score data has been reset")
                break
