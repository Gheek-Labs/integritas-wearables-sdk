"""
Health Monitoring Example
Real-time vital signs monitoring with tamper-proof timestamps
"""

import time
import random
from wearables_sdk import WearablesSDK

def simulate_heart_rate():
    """Simulate heart rate sensor (60-100 bpm)"""
    return random.randint(60, 100)

def simulate_spo2():
    """Simulate blood oxygen saturation (95-100%)"""
    return random.randint(95, 100)

def main():
    # Initialize SDK (replace with your actual API key)
    sdk = WearablesSDK(api_key="your_integritas_api_key_here")
    
    try:
        print("Starting health monitoring...")
        print("Recording vital signs every 30 seconds")
        
        for i in range(10):  # Record 10 readings
            # Record heart rate
            hr = simulate_heart_rate()
            hr_id = sdk.record_sensor_data(
                "heart_rate", 
                hr, 
                {
                    "unit": "bpm",
                    "sensor_type": "PPG",
                    "location": "wrist",
                    "confidence": 0.95
                }
            )
            print(f"Recorded heart rate: {hr} bpm (ID: {hr_id})")
            
            # Record SpO2
            spo2 = simulate_spo2()
            spo2_id = sdk.record_sensor_data(
                "blood_oxygen", 
                spo2, 
                {
                    "unit": "percent",
                    "sensor_type": "PPG",
                    "location": "wrist",
                    "confidence": 0.92
                }
            )
            print(f"Recorded SpO2: {spo2}% (ID: {spo2_id})")
            
            # Wait 30 seconds (in real app, this would be continuous)
            time.sleep(1)  # Reduced for demo
        
        # Wait for processing to complete
        time.sleep(2)
        
        # Retrieve and verify all data
        verified_data = sdk.get_verified_data()
        print(f"\nRetrieved {len(verified_data)} verified records:")
        
        for record in verified_data:
            is_valid = sdk.verify_timestamp(record)
            original = record['original_data']
            print(f"  {original['sensor_type']}: {original['value']} "
                  f"(Valid: {is_valid}, Timestamp: {record['timestamp']})")
        
        # Check system status
        status = sdk.get_status()
        print(f"\nSystem Status: {status}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sdk.shutdown()

if __name__ == "__main__":
    main()
