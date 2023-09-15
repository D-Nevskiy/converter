from django.db import models


class Currency(models.Model):
    """Модель валюты."""
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.code
