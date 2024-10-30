from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient
from django.urls import reverse
from .models import ExchangeRate
from unittest.mock import patch
from datetime import timedelta


class ExchangeRateTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("get_current_usd")

    @patch("requests.get")
    def test_get_current_usd_with_empty_db(self, mock_get):
        # Мок ответа API
        mock_get.return_value.json.return_value = {"rates": {"RUB": 75.0}}

        # Запрос к эндпоинту
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("current_rate", response.data)
        self.assertIn("last_10", response.data)
        self.assertEqual(response.data["current_rate"], 75.0)

    @patch("requests.get")
    def test_rate_update_interval(self, mock_get):
        # Добавим запись в базу данных
        ExchangeRate.objects.create(rate=75.0)
        last_record = ExchangeRate.objects.order_by("-timestamp").first()

        # Запросим курс снова без 10-секундной паузы
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["current_rate"], last_record.rate)

    @patch("requests.get")
    def test_last_10_entries(self, mock_get):
        # Добавляем 12 записей в базу данных
        for i in range(12):
            ExchangeRate.objects.create(
                rate=75.0 + i, timestamp=timezone.now() - timedelta(seconds=i * 15)
            )

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            len(response.data["last_10"]), 10
        )  # Убедимся, что возвращаются последние 10
