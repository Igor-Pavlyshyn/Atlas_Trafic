from rest_framework import serializers
from .models import Intersection, Safety, Efficiency


class IntersectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intersection
        fields = "__all__"


class SafetySerializer(serializers.ModelSerializer):

    class Meta:
        model = Safety
        fields = "__all__"


class EfficiencySerializer(serializers.ModelSerializer):

    class Meta:
        model = Efficiency
        fields = "__all__"
