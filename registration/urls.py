from django.urls import path, include
from rest_framework import routers

from .views import ParcelViewSet

router = (
    routers.DefaultRouter()
)  # получать менять удалять, получить список, добавить новую
router.register(r"parcels", ParcelViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls")),
]
