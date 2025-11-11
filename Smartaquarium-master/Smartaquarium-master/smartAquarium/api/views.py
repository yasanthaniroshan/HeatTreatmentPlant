from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import TemperatureReading, TemperatureSetpoint


@csrf_exempt
@require_http_methods(["POST"])
def receive_sensor_data(request):
    """
    Receive sensor data from Arduino in format:
    {WA:24.50, AI:26.20, HU:60.50, SP:25.00, PWR:120}
    """
    try:
        body = json.loads(request.body)
        
        # Extract data from request
        water_temp = float(body.get('WA', 0))
        air_temp = float(body.get('AI', 0))
        humidity = float(body.get('HU', 0))
        setpoint = float(body.get('SP', 0))
        pid_output = float(body.get('PWR', 0))
        
        # Save reading to database
        reading = TemperatureReading.objects.create(
            water_temperature=water_temp,
            air_temperature=air_temp,
            humidity=humidity,
            setpoint=setpoint,
            pid_output=pid_output
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Data received and saved',
            'reading_id': reading.id
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["GET"])
def get_latest_reading(request):
    """Get the latest temperature and humidity reading"""
    try:
        reading = TemperatureReading.objects.latest('timestamp')
        setpoint_obj = TemperatureSetpoint.get_or_create_default()
        
        return JsonResponse({
            'water_temperature': reading.water_temperature,
            'air_temperature': reading.air_temperature,
            'humidity': reading.humidity,
            'setpoint': setpoint_obj.setpoint,
            'pid_output': reading.pid_output,
            'timestamp': reading.timestamp.isoformat()
        })
    except TemperatureReading.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'No readings available'
        }, status=404)


@require_http_methods(["GET"])
def get_setpoint(request):
    """Get current temperature setpoint"""
    setpoint_obj = TemperatureSetpoint.get_or_create_default()
    
    return JsonResponse({
        'setpoint': setpoint_obj.setpoint,
        'min_setpoint': setpoint_obj.min_setpoint,
        'max_setpoint': setpoint_obj.max_setpoint
    })


@csrf_exempt
@require_http_methods(["POST"])
def set_setpoint(request):
    """Set new temperature setpoint"""
    try:
        body = json.loads(request.body)
        new_setpoint = float(body.get('setpoint'))
        
        setpoint_obj = TemperatureSetpoint.get_or_create_default()
        
        # Validate setpoint is within bounds
        if new_setpoint < setpoint_obj.min_setpoint or new_setpoint > setpoint_obj.max_setpoint:
            return JsonResponse({
                'status': 'error',
                'message': f'Setpoint must be between {setpoint_obj.min_setpoint} and {setpoint_obj.max_setpoint}'
            }, status=400)
        
        setpoint_obj.setpoint = new_setpoint
        setpoint_obj.save()
        
        return JsonResponse({
            'status': 'success',
            'setpoint': setpoint_obj.setpoint,
            'message': f'Setpoint updated to {new_setpoint}°C'
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)


@require_http_methods(["GET"])
def get_readings_history(request):
    """Get historical readings (last 50)"""
    readings = TemperatureReading.objects.all()[:50]
    
    data = [{
        'water_temperature': r.water_temperature,
        'air_temperature': r.air_temperature,
        'humidity': r.humidity,
        'setpoint': r.setpoint,
        'pid_output': r.pid_output,
        'timestamp': r.timestamp.isoformat()
    } for r in readings]
    
    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'readings': data
    })
