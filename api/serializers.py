from rest_framework import serializers

from currency.models import Currency


class CurrencySerializer(serializers.ModelSerializer):
    """Сериализатор для валюты"""

    class Meta:
        model = Currency
        fields = ('code', 'name')
