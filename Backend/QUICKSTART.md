# Quick Start Guide - Heat Treatment Plant Control

## 5-Minute Setup

### Step 1: Install Dependencies
```bash
cd "d:\Industrial Automation-Project\Smartaquarium-master\Smartaquarium-master\smartAquarium"
pip install -r requirements.txt
```

### Step 2: Setup Database
```bash
python manage.py migrate
python manage.py init_setpoint
```

### Step 3: Create Admin Account (Optional)
```bash
python manage.py createsuperuser
```

### Step 4: Start the Server
```bash
python manage.py runserver
```

### Step 5: Access the Application
- Open your browser and go to: **http://localhost:8000**
- Dashboard: **http://localhost:8000/backend/dashboard/**
- Settings: **http://localhost:8000/backend/settings/**

---

## Connecting Arduino

### Option 1: Using the Arduino Relay Script (Recommended)

1. **Install pyserial** (already in requirements.txt):
```bash
pip install pyserial
```

2. **Find your Arduino's COM port:**
   - Windows: Device Manager → Ports (COM & LPT)
   - Linux: `ls /dev/ttyUSB*` or `ls /dev/ttyACM*`

3. **Run the relay script:**
```bash
python arduino_relay.py --port COM3 --host http://localhost:8000
```

Replace `COM3` with your actual Arduino port.

4. **For remote server:**
```bash
python arduino_relay.py --port COM3 --host http://192.168.1.100:8000
```

### Option 2: Arduino Code Integration

Add this to your Arduino sketch to send data to the server:

```cpp
// In your Arduino setup():
Serial.begin(9600);

// In your Arduino loop():
// After reading sensors, send data as JSON
Serial.print("{WA:");
Serial.print(waterTemp, 2);
Serial.print(",AI:");
Serial.print(airTemp, 2);
Serial.print(",HU:");
Serial.print(humidity, 1);
Serial.print(",SP:");
Serial.print(setPoint, 2);
Serial.print(",PWR:");
Serial.print(pidOutput);
Serial.println("}");

// To receive setpoint updates from web interface:
if (Serial.available() > 0) {
  String incoming = Serial.readStringUntil('\n');
  incoming.trim();
  if (incoming.startsWith("SET:")) {
    float newSetpoint = incoming.substring(4).toFloat();
    setPoint = newSetpoint;
    // Update your PID setpoint here
  }
}
```

---

## Dashboard Features

### Real-Time Monitoring
- **Water Temperature**: Current tank water temperature
- **Air Temperature**: Room/ambient air temperature
- **Humidity**: Current humidity level
- **Setpoint**: Current target temperature
- **PID Output**: Control system status (Heating/Idle/Cooling)

### Temperature Control
- Set new setpoint directly from dashboard
- Range validation (15°C - 40°C)
- Real-time feedback

---

## Settings Page

### Configure Temperature Setpoint
- Adjust target temperature
- View hardware configuration
- Monitor control algorithm details
- Safety information

---

## API Usage

### Send Sensor Data
```bash
curl -X POST http://localhost:8000/api/sensor-data/ \
  -H "Content-Type: application/json" \
  -d '{"WA": 24.5, "AI": 26.2, "HU": 60.5, "SP": 25.0, "PWR": 120}'
```

### Get Latest Reading
```bash
curl http://localhost:8000/api/latest-reading/
```

### Get/Set Setpoint
```bash
# Get current setpoint
curl http://localhost:8000/api/setpoint/

# Set new setpoint
curl -X POST http://localhost:8000/api/setpoint/set/ \
  -H "Content-Type: application/json" \
  -d '{"setpoint": 27.5}'
```

---

## Troubleshooting

### Dashboard shows no data
1. Check if Arduino is connected: Look for incoming data in Arduino Serial Monitor
2. Run relay script: `python arduino_relay.py`
3. Check relay script logs: `cat arduino_relay.log`
4. Try sending test data via API:
   ```bash
   curl -X POST http://localhost:8000/api/sensor-data/ \
     -H "Content-Type: application/json" \
     -d '{"WA": 25.0, "AI": 25.0, "HU": 50.0, "SP": 25.0, "PWR": 0}'
   ```

### Port already in use
If Django reports port 8000 is in use:
```bash
python manage.py runserver 8001
```

### Arduino not found
- Check COM port in Device Manager
- Try: `python arduino_relay.py --port COM4 --host http://localhost:8000`
- Verify Arduino sketch is uploading and running

### Database errors
Reset and reinitialize:
```bash
del db.sqlite3
python manage.py migrate
python manage.py init_setpoint
```

---

## Production Deployment

For deploying to a Raspberry Pi or remote server:

1. **Install on server:**
```bash
cd /path/to/smartAquarium
pip install -r requirements.txt
python manage.py migrate
python manage.py init_setpoint
```

2. **Run with Gunicorn:**
```bash
pip install gunicorn
gunicorn smartAquarium.wsgi --bind 0.0.0.0:8000
```

3. **Relay script for remote:**
```bash
python arduino_relay.py --port COM3 --host http://your-server-ip:8000
```

---

## Next Steps

1. ✅ Set up Django server
2. ✅ Connect Arduino via relay script
3. ✅ Monitor data in dashboard
4. ✅ Adjust setpoint and test control
5. 📊 Review historical data (future feature)
6. 🔔 Set up alerts (future feature)

---

## Support Files

- `README.md` - Full documentation
- `arduino_relay.py` - Serial data relay script
- `api/models.py` - Database models
- `api/views.py` - REST API endpoints
- `templates/dashboard.html` - Main monitoring interface
- `templates/settings.html` - Settings interface

Enjoy your Heat Treatment Plant Control system! 🐠
