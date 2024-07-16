from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Intersection, Safety, Efficiency
from .serializers import SafetySerializer, IntersectionSerializer, EfficiencySerializer, IntersectionCreateSerializer


class IntersectionCreateView(generics.CreateAPIView):
    queryset = Intersection.objects.all()
    serializer_class = IntersectionCreateSerializer


class IntersectionView(generics.RetrieveAPIView):
    queryset = Intersection.objects.all()
    serializer_class = IntersectionSerializer
    lookup_field = "intersection_id"


class IntersectionEventUpdateView(APIView):
    def post(self, request, intersection_id):
        try:
            intersection = Intersection.objects.get(intersection_id=intersection_id)
        except Intersection.DoesNotExist:
            return Response(
                {"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND
            )

        safety, _ = Safety.objects.get_or_create(intersection=intersection)
        safety.update_safety(
            {
                "accident_rate": 1,
                "near_misses": 3,
                "speeding": 5,
                "traffic_violations": {
                    "tailgating": 2,
                    "red_light_running": 1,
                    "distracted_driving": 4,
                    "changing_lanes": 3
                },
                "pedestrian_incidents": {
                    "no_crosswalk_sign": 1,
                    "near_miss": 2,
                    "aggressive_behavior": 3
                },
                "damaged_disabled_vehicle": {
                    "stuck_in_lane": 1,
                    "broken_down_intersection": 1,
                    "broken_down_side": 1
                }
            }
        )

        efficiency, _ = Efficiency.objects.get_or_create(
            intersection=intersection
        )
        is_school_hours = request.data.get("is_school_hours", False)
        is_near_school = request.data.get("is_near_school", False)
        efficiency.update_efficiency(
            {
                "congestion_level": 55,
                "average_traffic_speed": {
                    "avg_speed": 45,
                    "min_speed_limit": 50,
                    "max_speed_limit": 60
                },
                "traffic_volume": 2100,
                "signal_timing_efficiency": 40,
                "pedestrian_wait_time": 40,
                "is_near_school": True,
                "is_school_hours": True,
                "micro_mobility_wait_time": 60
            },
            is_school_hours=True,
            is_near_school=True
        )

        efficiency_serializer = EfficiencySerializer(efficiency)
        safety_serializer = SafetySerializer(safety)
        return Response(
            {
                "efficiency": efficiency_serializer.data,
                "safety": safety_serializer.data,
            },
            status=status.HTTP_200_OK,
        )
