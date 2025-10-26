from wearables_sdk import WearablesSDK
from wearables_sdk.security import load_api_key

def on_overflow(item):
    print("[WARN] Queue overflow; consider reducing sampling:", item.get("id"))

def main():
    api_key = load_api_key()
    sdk = WearablesSDK(api_key, on_queue_overflow=on_overflow)
    try:
        sdk.record_sensor_data("heart_rate", 72, {"unit": "bpm"})
        print(sdk.get_status())
    finally:
        sdk.shutdown()

if __name__ == "__main__":
    main()
