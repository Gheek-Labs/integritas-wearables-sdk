"""
Fitness Tracking Example
Workout session tracking with immutable activity logs
"""

import time
import math
from wearables_sdk import WearablesSDK

class FitnessTracker:
    def __init__(self, api_key: str):
        self.sdk = WearablesSDK(api_key)
        self.session_id = f"workout_{int(time.time())}"
        self.steps = 0
        self.distance = 0.0
        self.calories = 0.0
        
    def start_workout(self, workout_type: str):
        """Start a new workout session"""
        self.sdk.record_sensor_data(
            "workout_start",
            workout_type,
            {
                "session_id": self.session_id,
                "start_time": time.time(),
                "workout_type": workout_type
            }
        )
        print(f"Started {workout_type} workout (Session: {self.session_id})")
    
    def record_step(self, step_count: int):
        """Record step count"""
        self.steps = step_count
        self.distance = step_count * 0.000762  # Average step length in km
        self.calories = self.distance * 60  # Approx calories per km
        
        self.sdk.record_sensor_data(
            "steps",
            step_count,
            {
                "session_id": self.session_id,
                "distance_km": round(self.distance, 2),
                "calories_burned": round(self.calories, 1),
                "timestamp": time.time()
            }
        )
    
    def record_heart_rate_zone(self, hr: int):
        """Record heart rate zone during workout"""
        if hr < 100:
            zone = "recovery"
        elif hr < 130:
            zone = "fat_burn"
        elif hr < 160:
            zone = "cardio"
        else:
            zone = "peak"
            
        self.sdk.record_sensor_data(
            "heart_rate_zone",
            hr,
            {
                "session_id": self.session_id,
                "zone": zone,
                "bpm": hr
            }
        )
    
    def end_workout(self):
        """End workout session"""
        self.sdk.record_sensor_data(
            "workout_end",
            self.session_id,
            {
                "session_id": self.session_id,
                "total_steps": self.steps,
                "total_distance_km": round(self.distance, 2),
                "total_calories": round(self.calories, 1),
                "end_time": time.time()
            }
        )
        print(f"Ended workout. Total: {self.steps} steps, {self.distance:.2f} km")
    
    def get_workout_summary(self):
        """Get verified workout summary"""
        verified = self.sdk.get_verified_data()
        workout_data = [r for r in verified if r['original_data'].get('session_id') == self.session_id]
        return workout_data
    
    def shutdown(self):
        self.sdk.shutdown()

def main():
    tracker = FitnessTracker("your_integritas_api_key_here")
    
    try:
        # Start running workout
        tracker.start_workout("running")
        
        # Simulate workout progress
        for minute in range(5):
            # Record steps (simulating 150 steps per minute)
            tracker.record_step(150 * (minute + 1))
            
            # Record heart rate (simulating increasing intensity)
            hr = 120 + (minute * 10)
            tracker.record_heart_rate_zone(hr)
            
            print(f"Minute {minute + 1}: {150 * (minute + 1)} steps, HR: {hr} bpm")
            time.sleep(0.5)  # Reduced for demo
        
        # End workout
        tracker.end_workout()
        
        # Wait for processing
        time.sleep(2)
        
        # Get verified summary
        summary = tracker.get_workout_summary()
        print(f"\nVerified workout records: {len(summary)}")
        for record in summary:
            original = record['original_data']
            print(f"  {original['sensor_type']}: {original.get('value', 'N/A')}")
    
    except Exception as e:
        print(f"Error: {e}")
    finally:
        tracker.shutdown()

if __name__ == "__main__":
    main()
