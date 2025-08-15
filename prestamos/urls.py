from rest_framework import routers
from django.urls import path, include
from .views import LoanViewSet, MembersViewSet

router = routers.DefaultRouter()
router.register(r"loans", LoanViewSet)
router.register(r"members", MembersViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
