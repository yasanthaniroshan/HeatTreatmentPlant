import requests
import time
import random
import serial


BASE_URL = "https://watertreatment.pythonanywhere.com/api/"
PORT = "/dev/ttyUSB0"
BAUDRATE = 9600


last_set_point:float = None

def read_sensor_data(ser:serial.Serial) -> dict:
    # ser = serial.Serial(PORT, BAUDRATE, timeout=1)
    # ser.flush()
    # line = ser.readline().decode('utf-8').rstrip()
    # ser.close()
    # parts = line.split(',')
    data = {
        "WA": round(random.uniform(20.0, 30.0), 2),
        "AI": round(random.uniform(20.0, 30.0), 2),
        "HU": round(random.uniform(40.0, 80.0), 2),
        "SP": round(random.uniform(20.0, 30.0), 2),
        "PWR": random.randint(100, 200)
    }
    return data

def send_set_point(ser:serial.Serial, set_point:float):
    # ser.flush()
    command = f"SET_POINT:{set_point}\n"
    # ser.write(command.encode('utf-8'))
    # ser.close()
    print(f"Sent to serial: {command.strip()}")

def send_data(data:dict):
    url = BASE_URL + "sensor-data/"
    response = requests.post(url, json=data)
    return response.json()

def get_set_point():
    url = BASE_URL + "setpoint/"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("setpoint")
    return None

if __name__ == "__main__":
    try:
        # ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        ser = None  # Placeholder for serial port
        while True:
            try:
                # sensor_data = read_sensor_data(ser)
                sensor_data = {
                    "WA": round(random.uniform(20.0, 30.0), 2),
                    "AI": round(random.uniform(20.0, 30.0), 2),
                    "HU": round(random.uniform(40.0, 80.0), 2),
                    "SP": round(random.uniform(20.0, 30.0), 2),
                    "PWR": random.randint(100, 200)
                }       
                print(f"Read sensor data: {sensor_data}")
                response = send_data(sensor_data)
                print(f"Sent data to server, response: {response}")

                set_point = get_set_point()
                if set_point is not None and set_point != last_set_point:
                    print(f"New set point received: {set_point}, sending to device.")
                    send_set_point(ser, set_point)
                    last_set_point = set_point

            except Exception as e:
                print(f"Error: {e}")

            time.sleep(2)  
    except serial.SerialException as e:
        print(f"Could not open serial port: {e}")
        exit(1)

    finally:
        if 'ser' in locals() and ser.is_open:
            ser.close()
