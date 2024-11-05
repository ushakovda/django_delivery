import json
import os
import django
import redis
from decimal import Decimal
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_delivery.settings')
django.setup()

import requests
from celery import shared_task
from django.core.cache import cache
from django.core.management.base import BaseCommand
from registration.models import Parcel

@shared_task
def fetch_exchange_rate():
    exchange_rate = cache.get('usd_to_rub')
    if exchange_rate is None:
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Проверка статуса ответа
            data = response.json()
            exchange_rate = str(data['Valute']['USD']['Value'])
            print(type(exchange_rate))
            print(exchange_rate)
            # Кешируем курс на 5 минут
            cache.set('usd_to_rub', exchange_rate, timeout=100)
        except Exception as e:
            print(f"Ошибка получения курса: {e}")
            return None
    return exchange_rate

@shared_task
def update_delivery_cost():
    exchange_rate = fetch_exchange_rate()

    if exchange_rate is None:
        print("Курс доллара не доступен.")
        return

    parcels = Parcel.objects.filter(delivery_cost_rub__isnull=True)

    for parcel in parcels:
        delivery_cost = (parcel.weight * Decimal(0.5) + parcel.content_value_usd * Decimal(0.01)) * Decimal(exchange_rate)
        parcel.delivery_cost_rub = round(delivery_cost, 2)
        parcel.save()

    print(f'Обновлены стоимости доставки для {len(parcels)} посылок.')

update_delivery_cost()

# class Command(BaseCommand):
#     help = 'Check Redis connection'
#
#     def handle(self, *args, **kwargs):
#         # Получаем настройки Redis из настроек Django
#         redis_host = 'redis'  # Замените на ваш хост
#         redis_port = 6379         # Замените на ваш порт
#
#         # Подключаемся к Redis
#         try:
#             r = redis.Redis(host=redis_host, port=redis_port)
#             r.ping()  # Проверка подключения
#             print(f"Connected to Redis at: {redis_host}:{redis_port}")
#         except redis.ConnectionError:
#             print("Failed to connect to Redis.")
#             return
#
#         # Проверка подключения через Django cache
#         cache.set('test_key', 'test_value', timeout=60)
#         value = cache.get('test_key')
#         if value == 'test_value':
#             self.stdout.write(self.style.SUCCESS('Successfully connected to Redis!'))
#         else:
#             self.stdout.write(self.style.ERROR('Failed to connect to Redis.'))
#

