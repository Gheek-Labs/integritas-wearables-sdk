# API Reference

## WearablesSDK Class

### `__init__(self, api_key: str)`
Initialize the SDK with your Integritas API key.

**Parameters:**
- `api_key` (str): Your Integritas Minima Global API key

**Raises:**
- `ValueError`: If API key is empty or None

### `record_sensor_data(self, sensor_type: str, value: Any, metadata: Dict = None) -> str`
Record sensor data for timestamping.

**Parameters:**
- `sensor_type` (str): Type of sensor (e.g., "heart_rate", "accelerometer")
- `value` (Any): Sensor reading value (numeric, string, or simple dict)
- `metadata` (Dict, optional): Additional context (max 1KB)

**Returns:**
- `str`: Unique ID for the recorded data point

**Raises:**
- `ValueError`: If metadata exceeds 1KB
- `RuntimeError`: If timestamp queue is full

### `get_verified_data(self) -> List[Dict]`
Get all successfully timestamped data with Integritas proofs.

**Returns:**
- `List[Dict]`: List of verified records containing:
  - `original_data`: Original sensor data
  - `hash`: SHA3-256 hash of the data
  - `timestamp`: Integritas timestamp
  - `proof`: Cryptographic proof of timestamp

### `verify_timestamp(self, data_record: Dict) -> bool`
Verify the integrity of a timestamped record.

**Parameters:**
- `data_record` (Dict): Record from `get_verified_data()`

**Returns:**
- `bool`: True if hash matches and proof exists

### `get_status(self) -> Dict[str, Any]`
Get current SDK operational status.

**Returns:**
- `Dict` containing:
  - `pending_requests`: Number of queued timestamp requests
  - `processed_count`: Number of successfully processed records
  - `platform`: Current platform identifier
  - `queue_full`: Boolean indicating if queue is at capacity

### `shutdown(self)`
Cleanly shutdown background processing threads.

## TimestampResponse Class

Dataclass returned by internal timestamp operations.

**Attributes:**
- `success` (bool): Whether timestamping succeeded
- `timestamp` (str, optional): ISO 8601 timestamp from Integritas
- `hash` (str, optional): SHA3 hash of the data
- `proof` (str, optional): Cryptographic proof
- `error` (str, optional): Error message if failed

## Platform Detection Constants

The SDK automatically detects the platform:

- `IS_ANDROID`: True on Wear OS devices
- `IS_IOS`: True on watchOS devices  
- `IS_TIZEN`: True on Tizen devices

## Hashing Implementation

All data is hashed using **SHA3-256** (FIPS 202 compliant):
- Uses Python 3.6+ `hashlib.sha3_256` when available
- Falls back to `pysha3` library for older Python versions
- Hashes compact JSON representation with sorted keys
- Uses UTF-8 encoding for consistent cross-platform results

## Threading Model

- **Main thread**: Handles sensor data recording (non-blocking)
- **Background thread**: Processes timestamp requests asynchronously
- **Thread-safe**: All public methods are thread-safe
- **Resource limits**: Queue limited to 100 items to prevent memory exhaustion

## Network Configuration

- **Timeouts**: 5s connect, 10s read (aggressive for wearables)
- **Connection pooling**: Reduced pool size for memory efficiency
- **Retry logic**: Maximum 2 retries for failed requests
- **Error handling**: Failed requests are logged but don't crash the application
