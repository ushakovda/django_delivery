from django.urls import path
from .views import ParcelCreateUpdateView, ParcelTypeListView

urlpatterns = [
    path('parcels/', ParcelCreateUpdateView.as_view(), name='parcel-create'),
    path('parcels/<int:pk>/', ParcelCreateUpdateView.as_view(), name='parcel-create'),
    path('parcel-types/', ParcelTypeListView.as_view(), name='parcel-type-list'),
]
