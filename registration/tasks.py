import requests
from celery import shared_task
from .models import Parcel

@shared_task
def fetch_exchange_rate():
    """Получает текущий курс доллара к рублю с сайта ЦБ РФ."""
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка статуса ответа
        data = response.json()
        return data['Valute']['USD']['Value']
    except Exception as e:
        print(f"Ошибка получения курса: {e}")
        return None

@shared_task
def update_delivery_cost():
    """Обновляет стоимость доставки для необработанных посылок."""
    exchange_rate = fetch_exchange_rate()

    if exchange_rate is None:
        print("Курс доллара не доступен.")
        return

    # Получаем все необработанные посылки
    parcels = Parcel.objects.filter(delivery_cost_rub__isnull=True)

    for parcel in parcels:
        # Вычисляем стоимость доставки по заданной формуле
        weight_kg = parcel.weight
        content_value_usd = parcel.content_value_usd

        delivery_cost = (weight_kg * 0.5 + content_value_usd * 0.01) * float(exchange_rate)
        parcel.delivery_cost_rub = round(delivery_cost, 2)
        parcel.save()

    print(f'Обновлены стоимости доставки для {len(parcels)} посылок.')
