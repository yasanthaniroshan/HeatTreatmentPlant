from django.contrib import admin
from .models import TemperatureReading, TemperatureSetpoint


@admin.register(TemperatureReading)
class TemperatureReadingAdmin(admin.ModelAdmin):
    list_display = ('water_temperature', 'air_temperature', 'humidity', 'setpoint', 'pid_output', 'timestamp')
    list_filter = ('timestamp',)
    search_fields = ('timestamp',)
    readonly_fields = ('timestamp',)
    ordering = ['-timestamp']


@admin.register(TemperatureSetpoint)
class TemperatureSetpointAdmin(admin.ModelAdmin):
    list_display = ('setpoint', 'min_setpoint', 'max_setpoint', 'updated_at')
    fields = ('setpoint', 'min_setpoint', 'max_setpoint')
    readonly_fields = ('updated_at',)
