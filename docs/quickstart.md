# Quick Start Guide

## Installation

### Using pip
```bash
pip install wearables-sdk
```

### From source
```bash
git clone https://github.com/yourusername/wearables-sdk.git
cd wearables-sdk
pip install -e .
```

## Basic Usage

### 1. Initialize the SDK
```python
from wearables_sdk import WearablesSDK

# Replace with your Integritas API key
sdk = WearablesSDK(api_key="your_integritas_api_key_here")
```

### 2. Record Sensor Data
```python
# Record heart rate
hr_id = sdk.record_sensor_data(
    "heart_rate", 
    72, 
    {"unit": "bpm", "location": "wrist"}
)

# Record accelerometer data
acc_id = sdk.record_sensor_data(
    "accelerometer",
    [0.1, -0.2, 9.8],
    {"frequency": "50Hz"}
)
```

### 3. Retrieve Verified Data
```python
# Get all timestamped data
verified_data = sdk.get_verified_data()

for record in verified_data:
    print(f"Sensor: {record['original_data']['sensor_type']}")
    print(f"Value: {record['original_data']['value']}")
    print(f"Timestamp: {record['timestamp']}")
    print(f"Proof: {record['proof'][:50]}...")
```

### 4. Verify Data Integrity
```python
# Verify individual record
is_valid = sdk.verify_timestamp(record)
print(f"Data integrity: {'VALID' if is_valid else 'INVALID'}")
```

### 5. Clean Shutdown
```python
sdk.shutdown()
```

## Platform-Specific Notes

### Wear OS (Android)
- Automatically checks network connectivity
- Uses Android's power management APIs
- Optimized for memory-constrained environments

### watchOS (iOS)
- Compatible with Python environments like Pyto
- Background task management for battery life
- Garbage collection optimized for real-time processing

### Tizen (Samsung Galaxy Watch)
- CPU wake lock management
- Platform-specific power optimizations
- Memory-efficient data structures

## Error Handling

The SDK handles common errors gracefully:

```python
try:
    hr_id = sdk.record_sensor_data("heart_rate", 72)
except ValueError as e:
    print(f"Invalid data: {e}")
except RuntimeError as e:
    print(f"System error: {e}")
```

Common errors:
- `ValueError`: Invalid API key or metadata too large
- `RuntimeError`: Queue full (data dropped due to memory constraints)
- Network errors are logged but don't raise exceptions

## Next Steps

- [API Reference](api_reference.md)
- [Platform Guide](platform_guide.md)  
- [Security Guide](security_guide.md)
- Check the [examples](../examples/) directory for complete use cases
