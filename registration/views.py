from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Parcel, ParcelType
from .serializers import ParcelSerializer, ParcelTypeSerializer


class ParcelCreateUpdateView(generics.CreateAPIView):
    serializer_class = ParcelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)  # создание записи в БД
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({"error": "ID не указан"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Parcel.objects.get(pk=pk)
        except Parcel.DoesNotExist:
            return Response({"error": "Неверный ID"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ParcelSerializer(instance=instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            return Response({"error": "ID не указан"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            instance = Parcel.objects.get(pk=pk)
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Parcel.DoesNotExist:
            return Response({"error": "Неверный ID"}, status=status.HTTP_404_NOT_FOUD)

class ParcelTypeListView(generics.ListAPIView):
    queryset = ParcelType.objects.all()
    serializer_class = ParcelTypeSerializer
