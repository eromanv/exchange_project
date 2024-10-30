from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import ExchangeRate
import requests
from django.utils import timezone
from datetime import timedelta

EXCHANGE_RATE_URL = "https://api.exchangerate-api.com/v4/latest/USD"  # Пример API


@api_view(["GET"])
def get_current_usd(request):
    # Получаем последнюю запись в базе данных
    last_record = ExchangeRate.objects.order_by("-timestamp").first()

    # Проверяем, прошло ли 10 секунд с момента последнего обновления
    if not last_record or timezone.now() > last_record.timestamp + timedelta(
        seconds=10
    ):
        response = requests.get(EXCHANGE_RATE_URL)
        data = response.json()
        usd_to_rub = data["rates"].get("RUB")

        # Создаем новую запись в базе данных
        ExchangeRate.objects.create(rate=usd_to_rub)

    # Получаем последние 10 записей
    last_10 = ExchangeRate.objects.order_by("-timestamp")[:10]
    return Response(
        {
            "current_rate": last_10[0].rate,
            "last_10": [
                {"rate": record.rate, "timestamp": record.timestamp}
                for record in last_10
            ],
        }
    )
