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
        session_id = request.COOKIES.get('session_id')
        parcel = serializer.save(session_id=session_id)

        # Устанавливаем session_id в куки, если его нет
        if hasattr(request, 'session_id'):
            response = Response({'id': parcel.id}, status=status.HTTP_201_CREATED)
            response.set_cookie('session_id', request.session_id)  # Устанавливаем cookie
            return response

        return Response({'id': parcel.id}, status=status.HTTP_201_CREATED)
