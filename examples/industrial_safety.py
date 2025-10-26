"""
Industrial Safety Example
Worker safety monitoring with tamper-proof incident logging
"""

import time
import random
from wearables_sdk import WearablesSDK

class SafetyMonitor:
    def __init__(self, api_key: str, worker_id: str, site_id: str):
        self.sdk = WearablesSDK(api_key)
        self.worker_id = worker_id
        self.site_id = site_id
        self.session_id = f"safety_{worker_id}_{int(time.time())}"
    
    def record_vital_signs(self, heart_rate: int, body_temp: float):
        """Record worker vital signs"""
        self.sdk.record_sensor_data(
            "worker_vitals",
            {
                "heart_rate": heart_rate,
                "body_temperature": body_temp
            },
            {
                "worker_id": self.worker_id,
                "site_id": self.site_id,
                "session_id": self.session_id,
                "alert_threshold_hr": 120,
                "alert_threshold_temp": 38.0
            }
        )
    
    def record_environmental_hazards(self, co_level: float, noise_level: int):
        """Record environmental hazard levels"""
        self.sdk.record_sensor_data(
            "environmental_hazards",
            {
                "carbon_monoxide_ppm": co_level,
                "noise_db": noise_level
            },
            {
                "worker_id": self.worker_id,
                "site_id": self.site_id,
                "session_id": self.session_id,
                "co_threshold": 35.0,
                "noise_threshold": 85
            }
        )
    
    def log_safety_incident(self, incident_type: str, severity: str, description: str):
        """Log safety incident with immutable timestamp"""
        incident_id = self.sdk.record_sensor_data(
            "safety_incident",
            incident_type,
            {
                "worker_id": self.worker_id,
                "site_id": self.site_id,
                "session_id": self.session_id,
                "severity": severity,
                "description": description,
                "timestamp": time.time(),
                "requires_investigation": severity in ["high", "critical"]
            }
        )
        return incident_id
    
    def record_location(self, x: float, y: float, z: float):
        """Record 3D location in facility"""
        self.sdk.record_sensor_data(
            "worker_location",
            {
                "x": x,
                "y": y,
                "z": z
            },
            {
                "worker_id": self.worker_id,
                "site_id": self.site_id,
                "session_id": self.session_id,
                "coordinate_system": "facility_local"
            }
        )
    
    def get_safety_log(self):
        """Get all verified safety records"""
        return self.sdk.get_verified_data()
    
    def shutdown(self):
        self.sdk.shutdown()

def main():
    safety = SafetyMonitor(
        api_key="your_integritas_api_key_here",
        worker_id="worker_12345",
        site_id="chemical_plant_alpha"
    )
    
    try:
        print("Starting industrial safety monitoring...")
        
        # Simulate normal operations
        for minute in range(3):
            # Record vitals
            hr = random.randint(65, 85)
            temp = round(random.uniform(36.1, 37.2), 1)
            safety.record_vital_signs(hr, temp)
            
            # Record environmental hazards
            co = round(random.uniform(5.0, 25.0), 1)
            noise = random.randint(70, 80)
            safety.record_environmental_hazards(co, noise)
            
            # Record location
            safety.record_location(
                random.uniform(0, 100),
                random.uniform(0, 50),
                random.uniform(0, 10)
            )
            
            print(f"Minute {minute + 1}: HR={hr}, Temp={temp}°C, CO={co}ppm")
            time.sleep(0.3)  # Reduced for demo
        
        # Simulate safety incident
        incident_id = safety.log_safety_incident(
            incident_type="chemical_spill",
            severity="high",
            description="Small acid spill detected in mixing area"
        )
        print(f"SAFETY INCIDENT LOGGED: {incident_id}")
        
        # Wait for processing
        time.sleep(2)
        
        # Get safety log
        safety_log = safety.get_safety_log()
        print(f"\nRetrieved {len(safety_log)} safety records:")
        
        incidents = [r for r in safety_log if r['original_data']['sensor_type'] == 'safety_incident']
        if incidents:
            print(f"SAFETY INCIDENTS FOUND: {len(incidents)}")
            for incident in incidents:
                original = incident['original_data']
                print(f"  Type: {original['value']}, Severity: {original['severity']}")
                print(f"  Description: {original['description']}")
                print(f"  Timestamp: {incident['timestamp']}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        safety.shutdown()

if __name__ == "__main__":
    main()
