from django.db import models

class Prices(models.Model):
    nobitex_currencies = models.CharField(max_length=255)
    wallex_currencies = models.CharField(max_length=255)
    common_currencies = models.CharField(max_length=255)

    class Meta:
        db_table = 'prices'
        managed = False  # Tell Django not to manage the table schema