#!/usr/bin/env python3
"""
Arduino Serial Data Relay - Bidirectional communication with Arduino and Django
This script acts as a bridge between Arduino and web server:
1. Receives sensor data from Arduino via Serial
2. Sends data to web server via HTTP POST
3. Reads setpoint updates from web server
4. Sends setpoint commands back to Arduino

This script runs on the Raspberry Pi that's connected to the Arduino.

Usage:
    python arduino_relay.py [--port COM3] [--baudrate 9600] [--host http://localhost:8000]

Examples:
    # Local server on same machine
    python arduino_relay.py --port COM3 --host http://localhost:8000
    
    # Remote server
    python arduino_relay.py --port /dev/ttyUSB0 --host http://192.168.1.100:8000
    
    # Different COM port
    python arduino_relay.py --port COM4
"""

import serial
import requests
import json
import argparse
import time
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('arduino_relay.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ArduinoRelay:
    """
    Bidirectional relay between Arduino and Django web server
    
    Flow:
    1. Arduino ──Serial──▶ Relay (sensor data)
    2. Relay ──HTTP──▶ Web Server (sensor data to database)
    3. Web Server ──API──▶ Relay (check for setpoint updates)
    4. Relay ──Serial──▶ Arduino (send setpoint commands)
    """
    
    def __init__(self, port='COM3', baudrate=9600, host='http://localhost:8000'):
        self.port = port
        self.baudrate = baudrate
        self.host = host
        
        # API endpoints
        self.sensor_data_endpoint = f"{host}/api/sensor-data/"
        self.setpoint_endpoint = f"{host}/api/setpoint/"
        
        self.ser = None
        self.running = False
        self.last_setpoint = None
        self.last_setpoint_check = time.time()
        
        logger.info(f"Initialized ArduinoRelay:")
        logger.info(f"  Serial Port: {port}")
        logger.info(f"  Baudrate: {baudrate}")
        logger.info(f"  Server: {host}")
    
    def connect(self):
        """Establish serial connection to Arduino"""
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # Wait for Arduino to reset
            logger.info(f"✓ Connected to Arduino on {self.port} at {self.baudrate} baud")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to connect to Arduino: {e}")
            return False
    
    def disconnect(self):
        """Close serial connection"""
        if self.ser:
            self.ser.close()
            logger.info("✓ Disconnected from Arduino")
    
    def parse_sensor_data(self, data_string):
        """
        Parse Arduino sensor data
        
        Format from Arduino: {WA:24.50,AI:26.20,HU:60.50,SP:25.00,PWR:120}
        
        Where:
        - WA = Water temperature (°C)
        - AI = Air temperature (°C)
        - HU = Humidity (%)
        - SP = Current setpoint (°C)
        - PWR = PID output power (-255 to +255)
        
        Returns: dict with keys: WA, AI, HU, SP, PWR
        """
        try:
            # Remove curly braces
            data_string = data_string.strip().strip('{}')
            
            # Parse key:value pairs separated by commas
            data = {}
            pairs = data_string.split(',')
            for pair in pairs:
                key, value = pair.split(':')
                data[key.strip()] = float(value.strip())
            
            # Validate required fields
            required = ['WA', 'AI', 'HU', 'SP', 'PWR']
            if all(k in data for k in required):
                return data
            else:
                logger.warning(f"✗ Incomplete data received (missing fields): {data_string}")
                return None
        except Exception as e:
            logger.warning(f"✗ Failed to parse sensor data: {data_string} - {e}")
            return None
    
    def send_sensor_data_to_server(self, data):
        """
        Send parsed sensor data to Django API
        
        POST /api/sensor-data/ with JSON data:
        {
            "WA": 24.50,    (water temperature)
            "AI": 26.20,    (air temperature)
            "HU": 60.50,    (humidity)
            "SP": 25.00,    (setpoint)
            "PWR": 120      (PID output)
        }
        """
        try:
            response = requests.post(
                self.sensor_data_endpoint,
                json=data,
                timeout=5
            )
            
            if response.status_code == 200:
                logger.debug(f"✓ Data → Server: WA={data['WA']}°C, AI={data['AI']}°C, HU={data['HU']}%")
                return True
            else:
                logger.warning(f"✗ Server error ({response.status_code}): {response.text}")
                return False
        
        except requests.exceptions.ConnectionError:
            logger.error(f"✗ Connection error: Cannot reach {self.sensor_data_endpoint}")
            return False
        except requests.exceptions.Timeout:
            logger.error("✗ Request timeout: Server not responding")
            return False
        except Exception as e:
            logger.error(f"✗ Error sending data: {e}")
            return False
    
    def get_setpoint_from_server(self):
        """
        Get current setpoint from web server
        
        GET /api/setpoint/ returns:
        {
            "setpoint": 25.00,
            "min_setpoint": 15.00,
            "max_setpoint": 40.00
        }
        """
        try:
            response = requests.get(
                self.setpoint_endpoint,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['setpoint']
            else:
                logger.warning(f"✗ Failed to get setpoint ({response.status_code})")
                return None
        
        except requests.exceptions.ConnectionError:
            logger.debug("✗ Cannot reach server (will retry)")
            return None
        except requests.exceptions.Timeout:
            logger.debug("✗ Server timeout (will retry)")
            return None
        except Exception as e:
            logger.warning(f"✗ Error getting setpoint: {e}")
            return None
    
    def send_setpoint_to_arduino(self, setpoint):
        """
        Send setpoint command to Arduino via Serial
        
        Format: SET:27.5
        
        Arduino will receive this in Serial buffer and execute:
        if (incoming.startsWith("SET:")) {
            setPoint = incoming.substring(4).toFloat();
            pidSetpoint = setPoint;
        }
        """
        try:
            command = f"SET:{setpoint}\n"
            self.ser.write(command.encode())
            logger.info(f"→ Arduino: SET:{setpoint}")
            return True
        except Exception as e:
            logger.error(f"✗ Failed to send to Arduino: {e}")
            return False
    
    def run(self):
        """
        Main loop - bidirectional relay
        
        Every cycle:
        1. Check for incoming sensor data from Arduino
        2. If data received, parse and send to server
        3. Periodically check server for setpoint updates
        4. If setpoint changed, send command to Arduino
        """
        if not self.connect():
            return
        
        self.running = True
        logger.info("╔════════════════════════════════════════════════════════════╗")
        logger.info("║     Heat Treatment Plant Control - Arduino Serial Relay Started         ║")
        logger.info("║                                                            ║")
        logger.info("║  Arduino ──Serial──▶ Relay ──HTTP──▶ Web Server            ║")
        logger.info("║                                                            ║")
        logger.info("║  Web Server ──API──▶ Relay ──Serial──▶ Arduino             ║")
        logger.info("║                                                            ║")
        logger.info("║  Press Ctrl+C to stop                                      ║")
        logger.info("╚════════════════════════════════════════════════════════════╝")
        
        try:
            while self.running:
                try:
                    # ===== RECEIVE FROM ARDUINO =====
                    if self.ser.in_waiting:
                        line = self.ser.readline().decode('utf-8').strip()
                        
                        if line:
                            logger.debug(f"◀ Arduino: {line}")
                            
                            # Parse sensor data
                            data = self.parse_sensor_data(line)
                            if data:
                                # Send to web server
                                self.send_sensor_data_to_server(data)
                    
                    # ===== CHECK FOR SETPOINT UPDATES (every 0.5 seconds) =====
                    current_time = time.time()
                    if current_time - self.last_setpoint_check >= 0.5:
                        self.last_setpoint_check = current_time
                        
                        # Get current setpoint from server
                        current_setpoint = self.get_setpoint_from_server()
                        
                        if current_setpoint is not None:
                            # If setpoint changed, send to Arduino
                            if self.last_setpoint != current_setpoint:
                                logger.info(f"Setpoint changed: {self.last_setpoint} → {current_setpoint}°C")
                                self.send_setpoint_to_arduino(current_setpoint)
                                self.last_setpoint = current_setpoint
                    
                    time.sleep(0.1)  # Small delay to prevent CPU spinning
                
                except UnicodeDecodeError as e:
                    logger.warning(f"✗ Decode error: {e}")
                except Exception as e:
                    logger.error(f"✗ Error in main loop: {e}")
                    time.sleep(1)  # Wait before retrying
        
        except KeyboardInterrupt:
            logger.info("\n✓ Received interrupt signal (Ctrl+C)")
        
        finally:
            self.disconnect()
            logger.info("═════════════════════════════════════════════════════════════")
            logger.info("     Arduino Relay Stopped")
            logger.info("═════════════════════════════════════════════════════════════")


def main():
    parser = argparse.ArgumentParser(
        description='Bidirectional relay between Arduino and Django web server'
    )
    parser.add_argument(
        '--port',
        default='COM3',
        help='Serial port for Arduino (default: COM3, Linux: /dev/ttyUSB0)'
    )
    parser.add_argument(
        '--baudrate',
        type=int,
        default=9600,
        help='Serial baudrate (default: 9600)'
    )
    parser.add_argument(
        '--host',
        default='http://localhost:8000',
        help='Django server URL (default: http://localhost:8000)'
    )
    
    args = parser.parse_args()
    
    relay = ArduinoRelay(
        port=args.port,
        baudrate=args.baudrate,
        host=args.host
    )
    
    relay.run()


if __name__ == '__main__':
    main()
