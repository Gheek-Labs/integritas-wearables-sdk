"""
Research Study Example
Clinical trial data collection with verifiable timestamps
"""

import time
import random
from datetime import datetime, timedelta
from wearables_sdk import WearablesSDK

class ResearchStudy:
    def __init__(self, api_key: str, study_id: str, participant_id: str):
        self.sdk = WearablesSDK(api_key)
        self.study_id = study_id
        self.participant_id = participant_id
        self.enrollment_date = datetime.utcnow().isoformat()
    
    def record_medication_adherence(self, medication_name: str, dose_mg: float, taken: bool):
        """Record medication adherence"""
        adherence_id = self.sdk.record_sensor_data(
            "medication_adherence",
            taken,
            {
                "study_id": self.study_id,
                "participant_id": self.participant_id,
                "medication_name": medication_name,
                "dose_mg": dose_mg,
                "scheduled_time": datetime.utcnow().isoformat(),
                "enrollment_date": self.enrollment_date,
                "protocol_version": "2.1"
            }
        )
        return adherence_id
    
    def record_symptom_severity(self, symptom: str, severity: int, notes: str = ""):
        """Record symptom severity (1-10 scale)"""
        if not 1 <= severity <= 10:
            raise ValueError("Severity must be 1-10")
            
        symptom_id = self.sdk.record_sensor_data(
            "symptom_severity",
            severity,
            {
                "study_id": self.study_id,
                "participant_id": self.participant_id,
                "symptom": symptom,
                "notes": notes,
                "timestamp": datetime.utcnow().isoformat(),
                "enrollment_date": self.enrollment_date,
                "protocol_version": "2.1"
            }
        )
        return symptom_id
    
    def record_daily_activity(self, steps: int, sleep_hours: float, mood_score: int):
        """Record daily activity metrics"""
        activity_id = self.sdk.record_sensor_data(
            "daily_activity",
            {
                "steps": steps,
                "sleep_hours": sleep_hours,
                "mood_score": mood_score
            },
            {
                "study_id": self.study_id,
                "participant_id": self.participant_id,
                "date": datetime.utcnow().date().isoformat(),
                "enrollment_date": self.enrollment_date,
                "protocol_version": "2.1"
            }
        )
        return activity_id
    
    def get_study_data(self):
        """Get all verified study data"""
        return self.sdk.get_verified_data()
    
    def export_for_analysis(self):
        """Export data in research-ready format"""
        verified_data = self.get_study_data()
        research_data = []
        
        for record in verified_data:
            original = record['original_data']
            research_record = {
                "participant_id": original['participant_id'],
                "study_id": original['study_id'],
                "data_type": original['sensor_type'],
                "value": original['value'],
                "timestamp": record['timestamp'],
                "verification_hash": record['hash'],
                "integritas_proof": record['proof']
            }
            research_data.append(research_record)
        
        return research_data
    
    def shutdown(self):
        self.sdk.shutdown()

def main():
    study = ResearchStudy(
        api_key="your_integritas_api_key_here",
        study_id="clinical_trial_xyz_2024",
        participant_id="pt_789012"
    )
    
    try:
        print("Starting clinical trial data collection...")
        
        # Simulate 3 days of data collection
        for day in range(3):
            print(f"\n--- Day {day + 1} ---")
            
            # Morning medication
            med_id = study.record_medication_adherence("Metformin", 500.0, True)
            print(f"Medication recorded: {med_id}")
            
            # Symptom check
            pain_severity = random.randint(1, 6)
            symptom_id = study.record_symptom_severity("joint_pain", pain_severity, "Worse in morning")
            print(f"Symptom recorded: severity {pain_severity}")
            
            # Daily activity
            steps = random.randint(3000, 8000)
            sleep = round(random.uniform(6.5, 8.5), 1)
            mood = random.randint(4, 9)
            activity_id = study.record_daily_activity(steps, sleep, mood)
            print(f"Activity recorded: {steps} steps, {sleep}h sleep, mood {mood}/10")
            
            time.sleep(0.5)  # Reduced for demo
        
        # Wait for processing
        time.sleep(2)
        
        # Export research data
        research_data = study.export_for_analysis()
        print(f"\nExported {len(research_data)} research records")
        
        # Show sample record
        if research_data:
            sample = research_data[0]
            print(f"\nSample Research Record:")
            print(f"  Participant: {sample['participant_id']}")
            print(f"  Data Type: {sample['data_type']}")
            print(f"  Value: {sample['value']}")
            print(f"  Timestamp: {sample['timestamp']}")
            print(f"  Verified: {'Yes' if sample['integritas_proof'] else 'No'}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        study.shutdown()

if __name__ == "__main__":
    main()
