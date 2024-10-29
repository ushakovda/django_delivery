from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet

from .models import Parcel, ParcelType
from .serializers import ParcelSerializer, ParcelTypeSerializer





class ParcelViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):

    queryset = Parcel.objects.all()
    serializer_class = ParcelSerializer

    @action(methods=['get'], detail=False)
    def types(self, request):
        parcel_types = ParcelType.objects.all()
        serializer = ParcelTypeSerializer(parcel_types, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        parcel = serializer.save()
        return Response({'id': parcel.id}, status=status.HTTP_201_CREATED)
