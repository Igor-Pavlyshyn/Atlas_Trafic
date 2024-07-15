from django.urls import path
from .views import (
    IntersectionSafetyView,
    IntersectionCreateView,
    IntersectionEventSafetyView,
    SafetyView
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
        IntersectionEventSafetyView.as_view(),
        name="intersection-event-update",
    ),
    path(
        "safety/<str:intersection_id>/",
        SafetyView.as_view(),
        name="safety",
    )
]
