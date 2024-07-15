from rest_framework import serializers
from .models import Intersection, Safety, Efficiency


class SafetySerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()
    accident_rate = serializers.SerializerMethodField()
    near_misses = serializers.SerializerMethodField()
    speeding = serializers.SerializerMethodField()
    traffic_violations = serializers.SerializerMethodField()
    pedestrian_incidents = serializers.SerializerMethodField()
    damaged_disabled_vehicle = serializers.SerializerMethodField()

    class Meta:
        model = Safety
        fields = "__all__"

    def get_points(self, obj):
        return obj.get_safety_grade()

    def get_total(self, obj):
        return (
                obj.accident_rate
                + obj.near_misses
                + obj.speeding
                + obj.traffic_violations
                + obj.pedestrian_incidents
                + obj.damaged_disabled_vehicle
        )

    def get_percentage(self, value, total):
        if total > 0:
            return (value / total) * 100
        return 0

    def get_accident_rate(self, obj):
        total = self.get_total(obj)
        return self.get_percentage(obj.accident_rate, total)

    def get_near_misses(self, obj):
        total = self.get_total(obj)
        return self.get_percentage(obj.near_misses, total)

    def get_speeding(self, obj):
        total = self.get_total(obj)
        return self.get_percentage(obj.speeding, total)

    def get_traffic_violations(self, obj):
        total = self.get_total(obj)
        return self.get_percentage(obj.traffic_violations, total)

    def get_pedestrian_incidents(self, obj):
        total = self.get_total(obj)
        return self.get_percentage(obj.pedestrian_incidents, total)

    def get_damaged_disabled_vehicle(self, obj):
        total = self.get_total(obj)
        return self.get_percentage(obj.damaged_disabled_vehicle, total)


class EfficiencySerializer(serializers.ModelSerializer):
    points = serializers.SerializerMethodField()

    class Meta:
        model = Efficiency
        fields = "__all__"

    def get_points(self, obj):
        return obj.get_efficiency_grade()


class IntersectionSerializer(serializers.ModelSerializer):
    safety_scores = SafetySerializer(many=True, read_only=True)
    efficiency_scores = EfficiencySerializer(many=True, read_only=True)

    class Meta:
        model = Intersection
        fields = (
            "id",
            "intersection_id",
            "coordinates",
            "condition",
            "safety_scores",
            "efficiency_scores",
        )


class IntersectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intersection
        fields = (
            "id",
            "intersection_id",
            "coordinates",
            "condition",
        )
