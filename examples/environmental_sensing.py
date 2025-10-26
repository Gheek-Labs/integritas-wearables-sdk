"""
Environmental Sensing Example
Air quality and temperature monitoring with verifiable timestamps
"""

import time
import random
from wearables_sdk import WearablesSDK

class EnvironmentalMonitor:
    def __init__(self, api_key: str, location: str):
        self.sdk = WearablesSDK(api_key)
        self.location = location
        self.device_id = f"env_sensor_{location}_{int(time.time())}"
    
    def read_temperature(self):
        """Simulate temperature reading (15-35°C)"""
        return round(random.uniform(15.0, 35.0), 1)
    
    def read_humidity(self):
        """Simulate humidity reading (30-80%)"""
        return round(random.uniform(30.0, 80.0), 1)
    
    def read_air_quality(self):
        """Simulate air quality index (0-500 AQI)"""
        return random.randint(0, 500)
    
    def record_environmental_data(self):
        """Record all environmental sensors"""
        temp = self.read_temperature()
        humidity = self.read_humidity()
        aqi = self.read_air_quality()
        
        # Record temperature
        temp_id = self.sdk.record_sensor_data(
            "temperature",
            temp,
            {
                "unit": "celsius",
                "location": self.location,
                "device_id": self.device_id,
                "sensor_type": "digital_thermistor"
            }
        )
        
        # Record humidity
        humidity_id = self.sdk.record_sensor_data(
            "humidity",
            humidity,
            {
                "unit": "percent",
                "location": self.location,
                "device_id": self.device_id,
                "sensor_type": "capacitive_humidity"
            }
        )
        
        # Record air quality
        aqi_id = self.sdk.record_sensor_data(
            "air_quality",
            aqi,
            {
                "unit": "aqi",
                "location": self.location,
                "device_id": self.device_id,
                "sensor_type": "particulate_matter",
                "pm25": random.randint(0, 150),
                "pm10": random.randint(0, 200)
            }
        )
        
        return {
            "temperature": temp,
            "humidity": humidity,
            "aqi": aqi,
            "ids": [temp_id, humidity_id, aqi_id]
        }
    
    def get_verified_readings(self):
        """Get all verified environmental readings"""
        return self.sdk.get_verified_data()
    
    def shutdown(self):
        self.sdk.shutdown()

def main():
    monitor = EnvironmentalMonitor(
        api_key="your_integritas_api_key_here",
        location="office_building_a"
    )
    
    try:
        print("Starting environmental monitoring...")
        print("Recording every 60 seconds (demo: every 2 seconds)")
        
        for i in range(5):  # 5 readings
            readings = monitor.record_environmental_data()
            print(f"Reading {i+1}: Temp={readings['temperature']}°C, "
                  f"Humidity={readings['humidity']}%, AQI={readings['aqi']}")
            time.sleep(0.5)  # Reduced for demo
        
        # Wait for processing
        time.sleep(2)
        
        # Get verified data
        verified = monitor.get_verified_readings()
        print(f"\nRetrieved {len(verified)} verified environmental readings:")
        
        for record in verified:
            original = record['original_data']
            print(f"  {original['sensor_type']}: {original['value']} "
                  f"(Location: {original['location']}, "
                  f"Timestamp: {record['timestamp']})")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        monitor.shutdown()

if __name__ == "__main__":
    main()
