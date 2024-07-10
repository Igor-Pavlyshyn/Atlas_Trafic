from django.urls import path
from .views import (
    IntersectionSafetyView,
    IntersectionCreateView,
    IntersectionEventUpdateView,
)

urlpatterns = [
    path(
        "intersections/<str:intersection_id>/safety/",
        IntersectionSafetyView.as_view(),
        name="intersection-safety",
    ),
    path(
        "intersections/create/",
        IntersectionCreateView.as_view(),
        name="intersection-create",
    ),
    path(
        "intersections/<str:intersection_id>/events/",
        IntersectionEventUpdateView.as_view(),
        name="intersection-event-update",
    ),
]
