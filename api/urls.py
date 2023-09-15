from django.urls import path
from .views import CurrencyConversion, CurrencyListCreateView

urlpatterns = [
    path('rates/', CurrencyConversion.as_view(), name='currency_conversion'),
    path('currency-list/', CurrencyListCreateView.as_view(), name='currency-list'),
]