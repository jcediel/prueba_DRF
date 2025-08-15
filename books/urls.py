from rest_framework import routers
from django.urls import path, include
from .views import BooksViewSet

router = routers.DefaultRouter()
router.register(r"books", BooksViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
