from django.db import models

# Create your models here.
class EquityData(models.Model):
    code = models.IntegerField()
    name = models.CharField(max_length=256)
    open = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()