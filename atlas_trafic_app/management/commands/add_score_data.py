from django.core.management.base import BaseCommand
from atlas_trafic_app.models import Safety, Efficiency, Environmental, Intersection


class Command(BaseCommand):
    help = "Add score data to the database"

    def handle(self, *args, **kwargs):
        safety_data = [
            {
                "intersection_id": i,
                "accident_rate": 1,
                "near_misses": 3,
                "speeding": 5,
                "traffic_violations": {
                    "tailgating": 2,
                    "red_light_running": 1,
                    "distracted_driving": 4,
                    "changing_lanes": 3,
                },
                "pedestrian_incidents": {
                    "no_crosswalk_sign": 1,
                    "near_miss": 2,
                    "aggressive_behavior": 3,
                },
                "damaged_disabled_vehicle": {
                    "stuck_in_lane": 1,
                    "broken_down_intersection": 1,
                    "broken_down_side": 1,
                },
            }
            for i in range(1, 3)
        ]
        Safety.objects.bulk_create([Safety(**data) for data in safety_data])

        efficiency_data = [
            {
                "intersection_id": i,
                "congestion_level": 55,
                "average_traffic_speed": {
                    "avg_speed": 45,
                    "min_speed_limit": 50,
                    "max_speed_limit": 60,
                },
                "traffic_volume": 2100,
                "signal_timing_efficiency": 40,
                "pedestrian_wait_time": 40,
                "is_near_school": True,
                "is_school_hours": True,
                "micro_mobility_wait_time": 60,
            }
            for i in range(1, 3)
        ]
        Efficiency.objects.bulk_create([Efficiency(**data) for data in efficiency_data])

        environmental_data = [
            {
                "intersection_id": i,
                "vehicle_emissions": 35,
                "fuel_consumption": 45,
                "noise_pollution": 80,
                "air_quality_index": 150,
                "driving_conditions": {"visibility": 0.3, "weather": "rain"},
                "fire_detection": 1,
            }
            for i in range(1, 3)
        ]
        Environmental.objects.bulk_create([Environmental(**data) for data in environmental_data])

        print("Data has been added")