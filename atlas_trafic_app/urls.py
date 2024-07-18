from django.urls import path
from .views import (
    IntersectionView,
    IntersectionCreateView,
    IntersectionEventUpdateView,
    IntersectionCarCreateView,
    IntersectionCarView
)

urlpatterns = [
    path(
        "intersections/<int:intersection_id>/",
        IntersectionView.as_view(),
        name="intersection-detail",
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
    path(
        "intersections/<int:intersection_id>/cars/",
        IntersectionCarCreateView.as_view(),
        name="intersection-cars",
    ),
    path(
        "intersections/<int:intersection_id>/cars/1/",
        IntersectionCarView.as_view(),
        name="intersection-car-detail",
    )
]
