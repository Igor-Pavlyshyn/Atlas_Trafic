from django.core.management.base import BaseCommand
from atlas_trafic_app.models import Car, Intersection
import random


class Command(BaseCommand):
    help = "Add car data to the database"

    def handle(self, *args, **kwargs):
        Car.objects.create(
            classification="Passenger Vehicle",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=1),
        )
        Car.objects.create(
            classification="Heavy Truck",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=1),
        )
        Car.objects.create(
            classification="Public Transportation",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=1),
        )
        Car.objects.create(
            classification="Pedestrian",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=1),
        )
        Car.objects.create(
            classification="Micromobility User",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=1),
        )

        Car.objects.create(
            classification="Passenger Vehicle",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=2),
        )
        Car.objects.create(
            classification="Heavy Truck",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=2),
        )
        Car.objects.create(
            classification="Public Transportation",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=2),
        )
        Car.objects.create(
            classification="Pedestrian",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=2),
        )
        Car.objects.create(
            classification="Micromobility User",
            count=random.randint(1, 12),
            intersection=Intersection.objects.get(id=2),
        )
