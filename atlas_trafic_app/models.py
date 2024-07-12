from django.db import models


class Intersection(models.Model):
    intersection_id = models.CharField(max_length=50, unique=True)
    coordinates = models.CharField(max_length=100)
    condition = models.CharField(max_length=50, default="Live")

    def update_intersection(self, data):
        if data.get("condition"):
            self.condition = data["condition"]

    def __str__(self):
        return f"{self.intersection_id} - {self.coordinates}"


class Safety(models.Model):
    intersection = models.ForeignKey(
        Intersection, on_delete=models.CASCADE, related_name="safety_scores"
    )
    points = models.FloatField(default=120)
    accident_rate = models.FloatField(default=0)
    near_misses = models.FloatField(default=0)
    speeding = models.FloatField(default=0)
    traffic_violations = models.FloatField(default=0)
    pedestrian_incidents = models.FloatField(default=0)
    damaged_disabled_vehicle = models.FloatField(default=0)

    def update_safety(self, data) -> None:
        if data.get("accident_rate"):
            self.accident_rate = data["accident_rate"] * 20

        if data.get("near_misses"):
            self.near_misses = data["near_misses"]

        if data.get("speeding"):
            self.speeding = data["speeding"] * 0.1

        traffic_violations = data.get("traffic_violations", {})
        self.traffic_violations = (
                traffic_violations.get("tailgating", 0) * 0.25 +
                traffic_violations.get("red_light_running", 0) * 0.25 +
                traffic_violations.get("distracted_driving", 0) * 0.25 +
                traffic_violations.get("changing_lanes", 0) * 0.25
        )

        pedestrian_incidents = data.get("pedestrian_incidents", {})
        self.pedestrian_incidents = (
                pedestrian_incidents.get("no_crosswalk_sign", 0) * 0.25 +
                pedestrian_incidents.get("near_miss", 0) * 0.25 +
                pedestrian_incidents.get("aggressive_behavior", 0) * 0.25
        )

        damaged_disabled_vehicle = data.get("damaged_disabled_vehicle", {})
        self.damaged_disabled_vehicle = (
                damaged_disabled_vehicle.get("stuck_in_lane", 0) * 5 +
                damaged_disabled_vehicle.get("broken_down_intersection", 0) * 5 +
                damaged_disabled_vehicle.get("broken_down_side", 0) * 5
        )

        self.save()
        self.calculate_safety_score()

    def calculate_safety_score(self) -> float:
        points_deducted = (
            self.accident_rate
            + self.near_misses
            + self.speeding
            + self.traffic_violations
            + self.pedestrian_incidents
            + self.damaged_disabled_vehicle
        )
        self.points = max(0, 120 - points_deducted)
        self.save()
        return self.points

    def get_safety_grade(self) -> str:
        score = self.points
        if score >= 100:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 60:
            return "C"
        elif score >= 40:
            return "D"
        else:
            return "F"

    def __str__(self) -> str:
        return f"{self.intersection.intersection_id} - Safety Score: {self.calculate_safety_score()}"
