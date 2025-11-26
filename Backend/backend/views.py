from django.shortcuts import render
from api.models import TemperatureReading, TemperatureSetpoint


def dashboard(request):
    """Display temperature and humidity dashboard"""
    try:
        latest_reading = TemperatureReading.objects.latest('timestamp')
    except TemperatureReading.DoesNotExist:
        latest_reading = None
    
    setpoint_obj = TemperatureSetpoint.get_or_create_default()
    
    context = {
        'latest_reading': latest_reading,
        'setpoint': setpoint_obj.setpoint,
        'min_setpoint': setpoint_obj.min_setpoint,
        'max_setpoint': setpoint_obj.max_setpoint,
    }
    
    return render(request, 'dashboard.html', context)


def settings(request):
    """Display settings page for temperature control"""
    setpoint_obj = TemperatureSetpoint.get_or_create_default()
    
    context = {
        'setpoint': setpoint_obj.setpoint,
        'min_setpoint': setpoint_obj.min_setpoint,
        'max_setpoint': setpoint_obj.max_setpoint,
    }
    
    return render(request, 'settings.html', context)
