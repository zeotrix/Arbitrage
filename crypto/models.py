from django.db import models

class Prices(models.Model):
    currency_id = models.IntegerField()   
    currencies = models.CharField(max_length=255)    
    binance_last_trade_price = models.FloatField()
    nobitex_last_trade_price = models.FloatField()
    wallex_last_trade_price = models.FloatField()
   

    class Meta:
        db_table = 'prices'
        managed = False  # Tell Django not to manage the table schema
    
    def __str__(self):
        return f"{self.currency_id} {self.currencies} {self.binance_last_trade_price} {self.nobitex_last_trade_price} {self.wallex_last_trade_price} "
    
    
