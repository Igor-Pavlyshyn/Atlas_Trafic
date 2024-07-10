from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Intersection, Safety, ScoreRating
from .serializers import SafetySerializer, IntersectionSerializer


class IntersectionCreateView(generics.CreateAPIView):
    queryset = Intersection.objects.all()
    serializer_class = IntersectionSerializer


class IntersectionSafetyView(APIView):
    def get(self, request, intersection_id):
        safety_scores = Safety.objects.filter(intersection__intersection_id=1234)
        for safety in safety_scores:
            safety.calculate_safety_score()
        serializer = SafetySerializer(safety_scores, many=True)
        return Response(serializer.data)


class IntersectionEventUpdateView(APIView):
    def post(self, request, intersection_id):
        try:
            intersection = Intersection.objects.get(intersection_id=intersection_id)
        except Intersection.DoesNotExist:
            return Response({"error": "Intersection not found."}, status=status.HTTP_404_NOT_FOUND)

        accident_rate = request.data.get("accident_rate", 0)
        near_misses = request.data.get("near_misses", 0)
        speeding = request.data.get("speeding", 0)
        traffic_violations = request.data.get("traffic_violations", 0)
        pedestrian_incidents = request.data.get("pedestrian_incidents", 0)
        damaged_disabled_vehicle = request.data.get("damaged_disabled_vehicle", 0)

        # Create or get ScoreRating instance
        score_rating, created = ScoreRating.objects.get_or_create(points=120)

        safety, created = Safety.objects.get_or_create(
            intersection=intersection,
            defaults={'score_rating': score_rating}
        )

        if not created:
            safety.score_rating = score_rating

        # safety.accident_rate = accident_rate
        # safety.near_misses = near_misses
        # safety.speeding = speeding
        # safety.traffic_violations = traffic_violations
        # safety.pedestrian_incidents = pedestrian_incidents
        # safety.damaged_disabled_vehicle = damaged_disabled_vehicle
        # safety.save()
        safety.update_safety(request.data)
        # Update safety score
        safety.calculate_safety_score()

        # Deduct points based on events
        # points_deducted = (
        #         accident_rate * 20 +
        #         near_misses * 1 +
        #         speeding * 0.1 +
        #         traffic_violations * 0.25 +
        #         pedestrian_incidents * 0.25 +
        #         damaged_disabled_vehicle * 5
        # )
        #
        # score_rating.points -= points_deducted
        # score_rating.save()

        serializer = SafetySerializer(safety)
        return Response(serializer.data, status=status.HTTP_200_OK)
