from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Intersection, Safety, Efficiency
from .serializers import SafetySerializer, IntersectionSerializer, EfficiencySerializer


class IntersectionCreateView(generics.CreateAPIView):
    queryset = Intersection.objects.all()
    serializer_class = IntersectionSerializer


class IntersectionSafetyView(generics.RetrieveAPIView):
    queryset = Intersection.objects.all()
    serializer_class = IntersectionSerializer
    lookup_field = "intersection_id"


class SafetyView(APIView):
    def get(self, request, intersection_id):
        try:
            safety = Safety.objects.get(intersection__intersection_id=intersection_id)
        except Safety.DoesNotExist:
            return Response({"error": "Safety not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = SafetySerializer(safety)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IntersectionEventSafetyView(APIView):
    def post(self, request, intersection_id):
        try:
            intersection = Intersection.objects.get(intersection_id=intersection_id)
        except Intersection.DoesNotExist:
            return Response({"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND)

        safety, created = Safety.objects.get_or_create(
            intersection=intersection
        )

        safety.update_safety(request.data)
        serializer = SafetySerializer(safety)
        return Response(serializer.data, status=status.HTTP_200_OK)


class IntersectionEventEfficiencyView(APIView):
    def post(self, request, intersection_id):
        try:
            intersection = Intersection.objects.get(intersection_id=intersection_id)
        except Intersection.DoesNotExist:
            return Response({"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND)

        efficiency, created = Efficiency.objects.get_or_create(
            intersection=intersection
        )

        is_school_hours = request.data.get("is_school_hours", False)
        is_near_school = request.data.get("is_near_school", False)

        efficiency.update_efficiency(request.data, is_school_hours, is_near_school)
        serializer = EfficiencySerializer(efficiency)
        return Response(serializer.data, status=status.HTTP_200_OK)
