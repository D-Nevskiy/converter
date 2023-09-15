from django.db.models import Q
from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from currency.models import Currency
from .serializers import CurrencySerializer


class CurrencyConversion(APIView):
    """
    View-класс предоставляет точку входа.
    Он парсит запрос, валидирует данные
    Возращает результат конвертации в ответе или сообщение об ошибке.

    """

    def get(self, request):
        from_currency_code = request.query_params.get('from')
        to_currency_code = request.query_params.get('to')
        amount = request.query_params.get('value')
        if not from_currency_code or not to_currency_code or not amount:
            return Response({'error': 'Требуются указание валют и количество: "from", "to" и "value"'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            amount = float(amount)
            if amount <= 0:
                return Response({'error': 'Количество должно быть больше 0'},
                                status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({'error': 'Неверный формат количества'},
                            status=status.HTTP_400_BAD_REQUEST)

        currencies = Currency.objects.filter(Q(code=from_currency_code) | Q(code=to_currency_code))

        if len(currencies) < 2:
            return Response(
                {'error': 'Неизвестный формат валюты. Весь список найти можно по endpoint: api/currency-list/'},
                status=status.HTTP_404_NOT_FOUND)

        result = self._convert_currency(from_currency_code, to_currency_code, amount)
        if not result:
            return Response({"error": "Ошибка при запросе к сервису"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'result': result}, status=status.HTTP_200_OK)

    def _convert_currency(self, from_currency_code, to_currency_code, amount):
        """
        Метод для отправки запроса к API сервиса конвертации валют.

        """
        api_url = f'https://api.exchangerate.host/convert?from={from_currency_code}&to={to_currency_code}&amount={amount}'
        try:
            response = requests.get(api_url)
            response.raise_for_status()
            data = response.json()
            return data.get('result')
        except requests.exceptions.RequestException as e:
            return None


class CurrencyListCreateView(generics.ListAPIView):
    """
    Дженерик для получения списка валют из базы данных.
    Возвращает список всех доступных валют.

    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
