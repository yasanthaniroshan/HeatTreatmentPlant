from django.db import models

class TemperatureReading(models.Model):
    """Model to store temperature and humidity readings from Arduino"""
    water_temperature = models.FloatField()
    air_temperature = models.FloatField()
    humidity = models.FloatField()
    setpoint = models.FloatField()
    pid_output = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"Reading at {self.timestamp}"


class TemperatureSetpoint(models.Model):
    """Model to store temperature setpoint configuration"""
    setpoint = models.FloatField(default=25.0)
    min_setpoint = models.FloatField(default=15.0)
    max_setpoint = models.FloatField(default=40.0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Temperature Setpoints"

    def __str__(self):
        return f"Setpoint: {self.setpoint}°C"

    @classmethod
    def get_or_create_default(cls):
        """Get or create default setpoint"""
        obj, created = cls.objects.get_or_create(
            id=1,
            defaults={'setpoint': 25.0}
        )
        return obj
