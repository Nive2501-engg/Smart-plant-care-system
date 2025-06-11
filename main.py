import Adafruit_DHT
import RPi.GPIO as GPIO
import time
from datetime import datetime

# Sensor and GPIO setup
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4  # GPIO pin for DHT22
SOIL_MOISTURE_PIN = 17  # GPIO pin (digital sensor or threshold module)
PUMP_RELAY_PIN = 27     # GPIO pin for pump relay

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SOIL_MOISTURE_PIN, GPIO.IN)
GPIO.setup(PUMP_RELAY_PIN, GPIO.OUT)
GPIO.output(PUMP_RELAY_PIN, GPIO.HIGH)  # Pump off by default

# Thresholds
MIN_SOIL_DRY = 0  # digital LOW (wet) vs HIGH (dry)
WATERING_DURATION = 5  # seconds

def log_data(temp, humidity, soil_state):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("plant_log.csv", "a") as file:
        file.write(f"{timestamp},{temp:.2f},{humidity:.2f},{soil_state}\n")

try:
    while True:
        # Read DHT sensor
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        # Read soil moisture (1 = dry, 0 = wet)
        soil_state = GPIO.input(SOIL_MOISTURE_PIN)

        print(f"Temp: {temperature:.1f}°C | Humidity: {humidity:.1f}% | Soil: {'Dry' if soil_state else 'Wet'}")

        # Water the plant if soil is dry
        if soil_state == 1:
            print("Soil is dry. Activating pump.")
            GPIO.output(PUMP_RELAY_PIN, GPIO.LOW)
            time.sleep(WATERING_DURATION)
            GPIO.output(PUMP_RELAY_PIN, GPIO.HIGH)
        else:
            print("Soil is moist. No watering needed.")

        log_data(temperature, humidity, "Dry" if soil_state else "Wet")

        time.sleep(60)  # Wait a minute before next read

except KeyboardInterrupt:
    print("Program stopped.")
    GPIO.cleanup()
