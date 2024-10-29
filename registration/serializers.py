from rest_framework import serializers
from .models import Parcel, ParcelType


class ParcelSerializer(serializers.ModelSerializer):
    parcel_type_name = serializers.CharField(write_only=True)  # Пользователь вводит название типа
    parcel_type = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Parcel
        fields = ['name', 'weight', 'content_value_usd', 'parcel_type_name', 'parcel_type', 'registered_at',
                  'delivery_cost_rub'] # Эти поля будем возвращать клиенту

    def create(self, validated_data):
        parcel_type_name = validated_data.pop('parcel_type_name')
        try:
            parcel_type = ParcelType.objects.get(name=parcel_type_name)  # Проверка существования типа
        except ParcelType.DoesNotExist:
            raise serializers.ValidationError({"parcel_type_name": "Указанный тип посылки не найден."})

        parcel = Parcel.objects.create(parcel_type=parcel_type, **validated_data)
        return parcel

    def update(self, instance, validated_data):
        parcel_type_name = validated_data.pop('parcel_type_name')
        try:
            parcel_type = ParcelType.objects.get(name=parcel_type_name)  # Проверка существования типа
        except ParcelType.DoesNotExist:
            raise serializers.ValidationError({"parcel_type_name": "Указанный тип посылки не найден."})

        instance.name = validated_data.get('name', instance.name)
        instance.weight = validated_data.get('weight', instance.weight)
        instance.content_value_usd = validated_data.get('content_value_usd', instance.content_value_usd)
        instance.parcel_type = parcel_type
        instance.registered_at = validated_data.get('registered_at', instance.registered_at)
        # instance.delivery_cost_rub = validated_data.get('delivery_cost_rub', instance.delivery_cost_rub)
        instance.save()
        return instance

class ParcelTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelType
        fields = '__all__'

''' Входные данные
{ 
    "name": "Одежда",
    "weight": "2.50",
    "content_value_usd": "100.00",
    "parcel_type_name": "Одежда"
}

Выходные данные
{
    "name": "Посылка 1",
    "weight": "2.50",
    "content_value_usd": "100.00",
    "parcel_type": 1,  # ID типа посылки
    "registered_at": "2024-10-26T12:00:00Z",  # Время регистрации
    "delivery_cost_rub": null  # Стоимость доставки (не рассчитана)
}
'''