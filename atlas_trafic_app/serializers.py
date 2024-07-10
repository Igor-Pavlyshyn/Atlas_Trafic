from rest_framework import serializers
from .models import Intersection, Safety, ScoreRating


class IntersectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Intersection
        fields = '__all__'


class ScoreRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScoreRating
        fields = '__all__'


class SafetySerializer(serializers.ModelSerializer):
    score_rating = ScoreRatingSerializer()

    class Meta:
        model = Safety
        fields = '__all__'

