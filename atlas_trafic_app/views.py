from collections import defaultdict
from datetime import time

from django.db.models import Sum
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Intersection, Safety, Efficiency, Environmental, Car
from .serializers import (
    SafetySerializer,
    IntersectionSerializer,
    EfficiencySerializer,
    IntersectionCreateSerializer,
    EnvironmentalSerializer,
    IntersectionCarInputSerializer,
    IntersectionCarResponseSerializer,
)


class IntersectionCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Intersection.objects.all()
    serializer_class = IntersectionCreateSerializer


class IntersectionView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Intersection.objects.all()
    serializer_class = IntersectionSerializer
    lookup_field = "intersection_id"


class IntersectionEventUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, intersection_id):
        try:
            intersection = Intersection.objects.get(intersection_id=intersection_id)
        except Intersection.DoesNotExist:
            return Response(
                {"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND
            )

        safety, _ = Safety.objects.get_or_create(intersection=intersection)
        safety.update_safety(request.data)

        efficiency, _ = Efficiency.objects.get_or_create(intersection=intersection)

        is_school_hours = request.data.get("is_school_hours", False)
        is_near_school = request.data.get("is_near_school", False)
        efficiency.update_efficiency(
            request.data,
            is_school_hours,
            is_near_school
        )

        environmental, _ = Environmental.objects.get_or_create(
            intersection=intersection
        )
        environmental.update_environmental(request.data)

        safety_serializer = SafetySerializer(safety)
        efficiency_serializer = EfficiencySerializer(efficiency)
        environmental_serializer = EnvironmentalSerializer(environmental)
        return Response(
            {
                "safety": safety_serializer.data,
                "efficiency": efficiency_serializer.data,
                "environmental": environmental_serializer.data,
            },
            status=status.HTTP_200_OK,
        )


class IntersectionCarCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, intersection_id):
        try:
            intersection = Intersection.objects.get(intersection_id=intersection_id)
        except Intersection.DoesNotExist:
            return Response({"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND)

        car_input_serializer = IntersectionCarInputSerializer(data=request.data)
        if car_input_serializer.is_valid():
            car_data = car_input_serializer.validated_data
            detected_at = timezone.now()
            classifications = defaultdict(int)

            total_cars = 0
            for classification, count in car_data.items():
                if count > 0:
                    Car.objects.create(
                        intersection=intersection,
                        classification=classification.replace("_", " "),
                        count=count,
                        detected_at=detected_at,
                    )
                    classifications[classification.replace("_", " ")] = count
                    total_cars += count

            response_data = {
                "total_cars": total_cars,
                "classifications": classifications,
                "detected_at": detected_at,
            }
            response_serializer = IntersectionCarResponseSerializer(response_data)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(car_input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class IntersectionCarView(APIView):
#     def get(self, request, intersection_id):
#         try:
#             intersection = Intersection.objects.get(intersection_id=intersection_id)
#         except Intersection.DoesNotExist:
#             return Response({"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND)
#         car_data_modifier = int(request.path.split("/")[-2][-1])  # Get the digit after the last '/' before 'cars'
#         if car_data_modifier == 1:
#             start_time = time(0, 0)  # 12:00 AM
#             end_time = time(12, 0)  # 12:00 PM
#         elif car_data_modifier == 2:
#             start_time = time(12, 0)  # 12:00 PM
#             end_time = time(23, 59)  # 11:59 PM
#         else:
#             return Response({"error": "Invalid car data modifier."}, status=status.HTTP_400_BAD_REQUEST)
#
#         cars = Car.objects.filter(intersection=intersection, detected_at__time__range=(start_time, end_time))
#         if not cars.exists():
#             return Response({"error": "No car data found for this intersection in the specified time range"},
#                             status=status.HTTP_404_NOT_FOUND)
#         total_cars = cars.aggregate(total=Sum('count'))['total']
#         classifications = cars.values('classification').annotate(count=Sum('count'))
#         detected_at = cars.latest('detected_at').detected_at
#         classification_counts = {entry['classification']: entry['count'] for entry in classifications}
#         response_data = {
#             "total_cars": total_cars,
#             "classifications": classification_counts,
#             "detected_at": f"from {start_time} to {end_time}",
#         }
#         return Response(response_data, status=status.HTTP_200_OK)

class IntersectionCarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, intersection_id):
        try:
            intersection = Intersection.objects.get(intersection_id=intersection_id)
        except Intersection.DoesNotExist:
            return Response({"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND)

        car_data_modifier = int(request.path.split("/")[-2][-1])  # Get the digit after the last '/' before 'cars'
        if car_data_modifier == 1:
            start_time = time(0, 0)  # 12:00 AM
            end_time = time(12, 0)  # 12:00 PM
        elif car_data_modifier == 2:
            start_time = time(12, 0)  # 12:00 PM
            end_time = time(23, 59)  # 12:00 AM
        else:
            return Response({"error": "Invalid car data modifier."}, status=status.HTTP_400_BAD_REQUEST)
        total_cars = Car.objects.filter(
            intersection=intersection,
            detected_at__time__gte=start_time,
            detected_at__time__lt=end_time
        ).aggregate(count=Sum('count'))['count']

        hourly_counts = {f'chart{chart_num}': 0 for chart_num in range(1, 13)}  # From chart1 to chart12
        # Filter and count cars for each hour in the 12-hour timeframe
        for hour, chart_num in zip(range(start_time.hour, end_time.hour), range(1, 13)):
            start_time = time(hour, 0)
            end_time = time(hour + 1, 0)
            if hour == 23:
                end_time = time(hour + 1, 59)
            count = Car.objects.filter(
                intersection=intersection,
                detected_at__time__gte=start_time,
                detected_at__time__lt=end_time
            ).aggregate(count=Sum('count'))['count']
            hourly_counts[f'chart{chart_num}'] = count if count else 0

        response_data = {
            "hourly_counts": hourly_counts,
            "total_cars": total_cars
        }
        return Response(response_data, status=status.HTTP_200_OK)


class IntersectionClassificationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, intersection_id):
        try:
            intersection = Intersection.objects.get(intersection_id=intersection_id)
        except Intersection.DoesNotExist:
            return Response({"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND)
        cars = Car.objects.filter(intersection=intersection)
        classifications = cars.values('classification').annotate(count=Sum('count'))
        classification_counts = {entry['classification'] for entry in classifications}
        return Response(classification_counts, status=status.HTTP_200_OK)
