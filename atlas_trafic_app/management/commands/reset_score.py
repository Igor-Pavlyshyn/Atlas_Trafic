from django.core.management.base import BaseCommand
from atlas_trafic_app.models import Safety, Efficiency, Environmental


class Command(BaseCommand):
    help = "Reset scores data in the database"

    def handle(self, *args, **kwargs):
        Safety.objects.update(
            points=120,
            accident_rate=0,
            near_misses=0,
            speeding=0,
            traffic_violations=0,
            pedestrian_incidents=0,
            damaged_disabled_vehicle=0
        )
        Efficiency.objects.update(
            points=120,
            congestion_level=0,
            average_traffic_speed=0,
            traffic_volume=0,
            signal_timing_efficiency=0,
            pedestrian_wait_time=0,
            micro_mobility_wait_time=0
        )
        Environmental.objects.update(
            points=120,
            vehicle_emissions=0,
            fuel_consumption=0,
            noise_pollution=0,
            air_quality_index=0,
            driving_conditions=0,
            fire_detection=0
        )

        print("Score data has been reset")
