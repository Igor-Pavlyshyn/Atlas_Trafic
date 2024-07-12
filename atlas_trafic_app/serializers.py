from rest_framework import serializers
from .models import Intersection, Safety


class IntersectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intersection
        fields = "__all__"


class SafetySerializer(serializers.ModelSerializer):

    class Meta:
        model = Safety
        fields = "__all__"
