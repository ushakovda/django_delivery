import uuid

from rest_framework import generics, mixins, status
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from common.models import UserSession
from .models import Parcel, ParcelType
from .serializers import ParcelSerializer, ParcelTypeSerializer

class ParcelViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
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
        session_id = request.session_id
        parcel = serializer.save(session_id=session_id)
        response = Response({'id': parcel.id}, status=status.HTTP_201_CREATED)
        if not request.COOKIES.get('session_id'):
            response.set_cookie('session_id', session_id)  # Устанавливаем cookie, если его нет

        return response

    def retrieve(self, request, *args, **kwargs):
        session_id_str = request.COOKIES.get('session_id')
        parcel_id = kwargs.get('pk')

        if not parcel_id:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            parcel = Parcel.objects.get(id=parcel_id)
        except Parcel.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            session_id = uuid.UUID(session_id_str)
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        if parcel.session_id != session_id:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = self.get_serializer(parcel)
        return Response(serializer.data)
