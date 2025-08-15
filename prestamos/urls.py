from rest_framework import routers
from django.urls import path, include
from .views import LoanViewSet, MembersViewSet, PenaltyViewSet, ReservationViewSet

router = routers.DefaultRouter()
router.register(r"loans", LoanViewSet)
router.register(r"members", MembersViewSet)
router.register(r"reservations", ReservationViewSet)
router.register(r"penalty", PenaltyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
