from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from atlas_trafic_app.models import Car, Intersection
import random


class Command(BaseCommand):
    help = "Add car data to the database"

    def handle(self, *args, **kwargs):
        for i in range(1, 3):
            Car.objects.create(
                classification="Passenger Vehicle",
                count=random.randint(1, 12),
                detected_at=datetime.now() + timedelta(hours=2),
                intersection=Intersection.objects.get(id=i),
            )
            Car.objects.create(
                classification="Heavy Truck",
                count=random.randint(1, 12),
                detected_at=datetime.now() + timedelta(hours=2),
                intersection=Intersection.objects.get(id=i),
            )
            Car.objects.create(
                classification="Public Transportation",
                count=random.randint(1, 12),
                detected_at=datetime.now() + timedelta(hours=2),
                intersection=Intersection.objects.get(id=i),
            )
            Car.objects.create(
                classification="Pedestrian",
                count=random.randint(1, 12),
                detected_at=datetime.now() + timedelta(hours=2),
                intersection=Intersection.objects.get(id=i),
            )
            Car.objects.create(
                classification="Micromobility User",
                count=random.randint(1, 12),
                detected_at=datetime.now() + timedelta(hours=2),
                intersection=Intersection.objects.get(id=i),
            )
            print(f"Added car data for intersection {i}")