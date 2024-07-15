from django.urls import path
from .views import (
    IntersectionView,
    IntersectionCreateView,
    IntersectionEventUpdateView,
)

urlpatterns = [
    path(
        "intersections/create/",
        IntersectionCreateView.as_view(),
        name="intersection-create",
    ),
    path(
        "intersections/<str:intersection_id>/",
        IntersectionView.as_view(),
        name="intersection-safety",
    ),
    path(
        "intersections/<str:intersection_id>/events/",
        IntersectionEventUpdateView.as_view(),
        name="intersection-event-update",
    )
]
