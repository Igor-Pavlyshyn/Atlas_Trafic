from rest_framework import serializers
from .models import Intersection, Safety, Efficiency


class SafetySerializer(serializers.ModelSerializer):

    class Meta:
        model = Safety
        fields = "__all__"


class IntersectionSerializer(serializers.ModelSerializer):
    safety_scores = SafetySerializer(many=True, read_only=True)
    class Meta:
        model = Intersection
        fields = ("id", "intersection_id", "coordinates", "condition", "safety_scores")


class EfficiencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Efficiency
        fields = "__all__"
