from django.urls import include, path
from . import views
from rest_framework import routers

app_name = "registration"

router = routers.DefaultRouter()
# router.register(r'registration', views.UserViewSet)
#
#
# urlpatterns = [
#     path('', include(router.urls)),
# ]
urlpatterns = [
    path('example/', views.example_view, name='example'),
    # Добавьте здесь другие пути, если они есть
]