from django.db import models


class Intersection(models.Model):
    intersection_id = models.CharField(max_length=50, unique=True)
    coordinates = models.CharField(max_length=100)
    condition = models.CharField(max_length=50, default="Live")

    def __str__(self):
        return f"{self.intersection_id} - {self.coordinates}"


class ScoreRating(models.Model):
    points = models.FloatField(default=120)

    def __str__(self):
        return f"Score: {self.points}"


class Safety(models.Model):
    intersection = models.ForeignKey(Intersection, on_delete=models.CASCADE, related_name='safety_scores')
    score_rating = models.ForeignKey(ScoreRating, on_delete=models.CASCADE, related_name='safety')
    accident_rate = models.IntegerField(default=0)
    near_misses = models.IntegerField(default=0)
    speeding = models.IntegerField(default=0)
    traffic_violations = models.IntegerField(default=0)
    pedestrian_incidents = models.IntegerField(default=0)
    damaged_disabled_vehicle = models.IntegerField(default=0)

    def update_safety(self, data):
        if data.get('accident_rate'):
            self.accident_rate = data['accident_rate']
        if data.get('near_misses'):
            self.near_misses = data['near_misses']
        if data.get('speeding'):
            self.speeding = data['speeding']
        if data.get('traffic_violations'):
            self.traffic_violations = data['traffic_violations']
        if data.get('pedestrian_incidents'):
            self.pedestrian_incidents = data['pedestrian_incidents']
        if data.get('damaged_disabled_vehicle'):
            self.damaged_disabled_vehicle = data['damaged_disabled_vehicle']
        self.save()
        self.calculate_safety_score()

    def calculate_safety_score(self):
        points_deducted = (
            self.accident_rate +
            self.near_misses +
            self.speeding +
            self.traffic_violations +
            self.pedestrian_incidents +
            self.damaged_disabled_vehicle
        )
        self.score_rating.points = 120 - points_deducted
        self.score_rating.save()
        return self.score_rating.points

    def get_safety_grade(self):
        score = self.calculate_safety_score()
        if score >= 100:
            return 'A'
        elif score >= 80:
            return 'B'
        elif score >= 60:
            return 'C'
        elif score >= 40:
            return 'D'
        else:
            return 'F'

    def __str__(self):
        return f"{self.intersection.intersection_id} - Safety Score: {self.calculate_safety_score()}"

