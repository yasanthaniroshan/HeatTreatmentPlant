from django.db import models

class FeedingMods(models.TextChoices):
    DEFAULT = 'Default'
    MOD_A = 'ModA'
    MOD_B = 'ModB'


class LightMods(models.TextChoices):
    OFF = 'Off' 
    RED = 'Red'
    GREEN = 'Green'
    BLUE = 'Blue'
    MOONLIGHT = 'Moonlight'

class AquariumParameters(models.model):
    tempurature = models.FloatField(verbose_name="Tempurature")
    pH = models.FloatField(verbose_name="pH")
    waterLevel = models.FloatField(verbose_name="Water Level")
    humidity = models.FloatField(verbose_name="Humidity")

class AquariumControls(models.model):
    isOpenedAirPump = models.BooleanField(verbose_name="Is Opened Air Pump",default=True)
    isOpenedWaterPump = models.BooleanField(verbose_name="Is Opened Water Pump",default=False)
    feedingMod = models.CharField(verbose_name="Feeding Mod",max_length=5,choices=FeedingMods.choices,default=FeedingMods.DEFAULT)
    isOpenedLight = models.BooleanField(verbose_name="Is Opened Light",default=False)
    isOpendedRGB = models.CharField(verbose_name="Is Opened RGB",max_length=5,choices=LightMods.choices,default=LightMods.OFF)


class EnemyDictected(models.model):
    enemy = models.TextField(verbose_name="Enemy")


