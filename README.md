# Wearables SDK (Hardened Release)

Secure edge timestamping for wearable devices using Integritas Minima Global API with SHA3 hashing.

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://www.python.org/)

## Features

- ✅ **SHA3-256 Hashing**: FIPS 202 compliant cryptographic hashing
- 🌐 **Cross-Platform**: Optimized for Wear OS, watchOS, and Tizen
- ⚡ **Edge Processing**: Timestamp data locally before transmission
- 🔒 **Secure**: API key authentication and immutable proofs
- 🔋 **Battery Efficient**: Background processing with power management
- 📱 **Resource Aware**: Memory-constrained queue system

## Quick Start

```python
from wearables_sdk import WearablesSDK

# Initialize with your Integritas API key
sdk = WearablesSDK(api_key="your_api_key_here")

# Record sensor data
hr_id = sdk.record_sensor_data("heart_rate", 72, {"unit": "bpm"})

# Get verified timestamped data
verified_data = sdk.get_verified_data()
```

## Installation

```bash
pip install wearables-sdk
# OR
pip install git+https://github.com/yourusername/wearables-sdk.git
```

## Requirements

- Python 3.6+
- `requests` library
- `pysha3` (for Python < 3.6)

## Supported Platforms

- **Wear OS** (Android 8.0+)
- **watchOS** (via Python environments like Pyto)
- **Tizen** (Samsung Galaxy Watch)
- **Generic Linux** (Raspberry Pi, etc.)

## Documentation

- [Quick Start Guide](docs/quickstart.md)
- [API Reference](docs/api_reference.md)
- [Platform Guide](docs/platform_guide.md)
- [Security Guide](docs/security_guide.md)

## Examples

See the `examples/` directory.

---

## Security Hardening (This Release)
- Enforced compact JSON with `allow_nan=False` for deterministic hashing
- Optional **TLS certificate pinning** via SHA-256 fingerprint preflight
- `on_queue_overflow` hook to react to queue pressure (reduce sampling, log, persist)
- Safe auto-shutdown in `__del__` to avoid background thread leaks
- `requests>=2.31.0` and Python `.gitignore` included
- New helpers in `wearables_sdk.security`:
  - `load_api_key()` (env or secure file)
  - `ensure_json_compact()`
  - `sha256_cert_fingerprint()`, `matches_any_fingerprint()`

## License

MIT License - see [LICENSE](LICENSE) for details.
