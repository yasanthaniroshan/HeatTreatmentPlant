from django.urls import path
from . import views

urlpatterns = [
    path('sensor-data/', views.receive_sensor_data, name='receive_sensor_data'),
    path('latest-reading/', views.get_latest_reading, name='get_latest_reading'),
    path('setpoint/', views.get_setpoint, name='get_setpoint'),
    path('setpoint/set/', views.set_setpoint, name='set_setpoint'),
    path('readings-history/', views.get_readings_history, name='get_readings_history'),
]
