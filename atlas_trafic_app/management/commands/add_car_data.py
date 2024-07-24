from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from atlas_trafic_app.models import Car, Intersection
import random


class Command(BaseCommand):
    help = "Add car data to the database"

    def handle(self, *args, **kwargs):
        intersections = Intersection.objects.all()
        for intersection in intersections:
            classifications = ["Passenger Vehicle",
                               "Heavy Truck",
                               "Public Transportation",
                               "Pedestrian",
                               "Micromobility User"]
            for classification in classifications:
                count = random.randint(1, 12)
                Car.objects.create(
                    classification=classification,
                    count=count,
                    intersection=intersection,
                )
            print(f"Added car data for intersection {intersection.id}")
