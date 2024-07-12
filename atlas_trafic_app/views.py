from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Intersection, Safety
from .serializers import SafetySerializer, IntersectionSerializer


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


class IntersectionEventUpdateView(APIView):
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
