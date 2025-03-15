from django.db import models

class Prices(models.Model):
    nobitex_currencies = models.CharField(max_length=255)
    wallex_currencies = models.CharField(max_length=255)
    common_currencies = models.CharField(max_length=255)

    class Meta:
        db_table = 'prices'
        managed = False  # Tell Django not to manage the table schema
    
    def __str__(self):
        return f"{self.nobitex_currencies} {self.wallex_currencies} {self.common_currencies}"
    
    
