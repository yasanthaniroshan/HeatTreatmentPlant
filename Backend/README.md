# Heat Treatment Plant Control - Temperature Control System

A web-based temperature and humidity monitoring and control system for aquarium environments, featuring real-time data visualization and PID-based temperature control.

## Features

✅ **Real-time Monitoring**
- Live water temperature readings (DS18B20 sensor)
- Air temperature monitoring (DHT22 sensor)
- Humidity level tracking
- PID output visualization

✅ **Temperature Control**
- Set custom target temperature setpoint (15°C - 40°C)
- Automatic heating/cooling with PID controller
- Time-proportional control (5-second window)
- Safe operation with configurable limits

✅ **Web Dashboard**
- Beautiful, responsive UI
- Real-time data updates (every 2 seconds)
- Historical data tracking
- Mobile-friendly interface

✅ **System Settings**
- Configure temperature setpoints
- View hardware configuration
- Monitor PID control parameters
- Safety information and alerts

## Architecture

### Backend Stack
- **Framework**: Django 3.2.6
- **Database**: SQLite
- **Python Version**: 3.7+

### Hardware Integration
- **Microcontroller**: Arduino Uno (ATmega328P)
- **Water Temp Sensor**: DS18B20 (One-Wire, Pin 6)
- **Air Sensor**: DHT22 (Pin 7) - Temperature & Humidity
- **Heater Control**: Relay on Pin 8 (Active LOW)
- **Fan/Cooler**: Relay on Pin 9 (Active LOW)
- **Display**: I2C LCD 16x2 (Address 0x27)
- **Communication**: Serial at 9600 baud

## Installation

### Prerequisites
- Python 3.7 or higher
- Django 3.2.6
- Git

### Steps

1. **Navigate to the project directory**
```bash
cd "d:\Industrial Automation-Project\Smartaquarium-master\Smartaquarium-master\smartAquarium"
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

If `requirements.txt` doesn't exist, create it with:
```
Django==3.2.6
```

3. **Apply database migrations**
```bash
python manage.py migrate
```

4. **Initialize default setpoint**
```bash
python manage.py init_setpoint
```

5. **Create a superuser (admin) account**
```bash
python manage.py createsuperuser
```

6. **Collect static files**
```bash
python manage.py collectstatic --noinput
```

## Running the Application

### Development Server

Start the Django development server:
```bash
python manage.py runserver
```

The application will be available at:
- **Home**: http://localhost:8000/
- **Dashboard**: http://localhost:8000/backend/dashboard/
- **Settings**: http://localhost:8000/backend/settings/
- **Admin Panel**: http://localhost:8000/admin/

### Production Deployment

For production deployment, use a production WSGI server like Gunicorn:
```bash
pip install gunicorn
gunicorn smartAquarium.wsgi
```

## API Endpoints

The system provides REST API endpoints for Arduino integration and data retrieval:

### Receive Sensor Data
**POST** `/api/sensor-data/`

Request format:
```json
{
    "WA": 24.50,
    "AI": 26.20,
    "HU": 60.50,
    "SP": 25.00,
    "PWR": 120
}
```

### Get Latest Reading
**GET** `/api/latest-reading/`

Response:
```json
{
    "water_temperature": 24.50,
    "air_temperature": 26.20,
    "humidity": 60.50,
    "setpoint": 25.00,
    "pid_output": 120,
    "timestamp": "2024-01-15T10:30:45Z"
}
```

### Get Current Setpoint
**GET** `/api/setpoint/`

Response:
```json
{
    "setpoint": 25.00,
    "min_setpoint": 15.00,
    "max_setpoint": 40.00
}
```

### Set New Setpoint
**POST** `/api/setpoint/set/`

Request:
```json
{
    "setpoint": 26.50
}
```

### Get Readings History
**GET** `/api/readings-history/`

Returns the last 50 readings with all sensor data.

## Arduino Integration

### Serial Communication Protocol

The Arduino sends sensor data every 2 seconds in the following format:
```
{WA:24.50,AI:26.20,HU:60.50,SP:25.00,PWR:120}
```

Fields:
- **WA**: Water temperature (°C)
- **AI**: Air temperature (°C)
- **HU**: Humidity (%)
- **SP**: Current setpoint (°C)
- **PWR**: PID output (-255 to +255)

### Receiving Commands

The system can send commands to the Arduino to update the setpoint:
```
SET:28.5
```

When a new setpoint is set via the web interface, it's automatically sent to the Arduino via Serial.

## Database Models

### TemperatureReading
Stores individual sensor readings:
- `water_temperature`: Float value in °C
- `air_temperature`: Float value in °C
- `humidity`: Float value in %
- `setpoint`: Target temperature (°C)
- `pid_output`: Current PID control output (-255 to +255)
- `timestamp`: DateTime of the reading

### TemperatureSetpoint
Stores configuration for temperature control:
- `setpoint`: Current target temperature (default: 25.0°C)
- `min_setpoint`: Minimum allowed setpoint (default: 15.0°C)
- `max_setpoint`: Maximum allowed setpoint (default: 40.0°C)
- `updated_at`: Last modification time

## Web Interface

### Dashboard
The main monitoring interface featuring:
- Large, easy-to-read sensor value cards
- Color-coded status indicators
- Real-time PID output display
- Interactive setpoint control
- Last update timestamp

### Settings Page
Configuration interface with:
- Temperature setpoint adjustment with range validation
- Hardware configuration information
- PID control algorithm details
- Safety limits and information
- System monitoring status

## Troubleshooting

### No data appearing in dashboard
1. Check if Arduino is connected and sending data via Serial
2. Verify the serial communication is working: `python manage.py shell`
   ```python
   from api.models import TemperatureReading
   TemperatureReading.objects.count()
   ```
3. Check Django logs for API errors

### Database errors
1. Reset the database: `rm db.sqlite3 && python manage.py migrate`
2. Reinitialize setpoint: `python manage.py init_setpoint`

### Arduino not receiving setpoint updates
1. Check serial connection is active
2. Verify Arduino is listening on Serial.available()
3. Check Arduino serial monitor to confirm reception

## File Structure

```
smartAquarium/
├── api/
│   ├── models.py           # Data models
│   ├── views.py            # API endpoints
│   ├── urls.py             # API routing
│   ├── admin.py            # Admin configuration
│   └── management/
│       └── commands/
│           └── init_setpoint.py   # Initialization command
├── backend/
│   ├── models.py
│   ├── views.py            # Dashboard views
│   ├── urls.py             # Backend routing
│   └── admin.py
├── smartAquarium/
│   ├── settings.py         # Django settings
│   ├── urls.py             # Main URL configuration
│   ├── wsgi.py             # WSGI application
│   └── views.py            # Home page view
├── templates/
│   ├── home.html           # Landing page
│   ├── dashboard.html      # Monitoring dashboard
│   └── settings.html       # Settings page
├── static/
│   ├── css/
│   │   └── home.css
│   └── img/
├── manage.py
├── db.sqlite3              # SQLite database
└── platformio.ini          # PlatformIO configuration (Arduino)
```

## Configuration

### Django Settings
Edit `smartAquarium/settings.py` to customize:
- Database backend (default: SQLite)
- Allowed hosts
- Static files directory
- Time zone (default: UTC)

### Arduino PID Parameters
Edit the Arduino code to adjust PID tuning:
```cpp
double Kp = 100, Ki = 5, Kd = 2;
```

## Performance Considerations

- Sensor readings: Every 2 seconds
- Data storage: All readings are stored (consider archiving old data)
- Database queries: Optimized with indexing on timestamp
- Web requests: CSRF protection enabled

## Security Notes

⚠️ **Development Only**: The current setup uses Django's development settings.

For production deployment:
1. Set `DEBUG = False` in settings.py
2. Configure proper `ALLOWED_HOSTS`
3. Use HTTPS
4. Store `SECRET_KEY` in environment variables
5. Use a production database (PostgreSQL recommended)
6. Implement proper authentication/authorization

## Future Enhancements

- [ ] Data logging and export (CSV, JSON)
- [ ] Historical graphs with Chart.js
- [ ] Email/SMS alerts for temperature anomalies
- [ ] Multi-tank support
- [ ] User authentication and role-based access
- [ ] API authentication tokens
- [ ] Data retention policies
- [ ] Mobile app integration

## Support

For issues or questions, please check:
1. Arduino code in `../../../ArduinoCode1106/src/main.cpp`
2. Django logs during development
3. Browser console for JavaScript errors
4. Django admin panel for data verification

## License

This project is part of the Industrial Automation project suite.

## Version History

- **v1.0** - Initial release with real-time monitoring and setpoint control
