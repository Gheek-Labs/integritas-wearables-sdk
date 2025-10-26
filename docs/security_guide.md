# Security Guide

## Cryptographic Implementation

### SHA3-256 Hashing
- **Algorithm**: SHA3-256 (FIPS 202 compliant)
- **Implementation**: Python standard library (3.6+) or pysha3 fallback
- **Data Format**: Compact JSON with sorted keys and no whitespace
- **Encoding**: UTF-8 for consistent cross-platform results

### Data Integrity
The SDK ensures data integrity through:
1. **Local Hashing**: Data hashed on-device before transmission
2. **Immutable Proofs**: Integritas provides cryptographic proofs
3. **Verification**: SDK can verify hash integrity locally
4. **Tamper Detection**: Any data modification invalidates the hash

### Example Verification Process
```python
# Original data
original_data = {"heart_rate": 72, "unit": "bpm"}

# SDK creates hash: sha3_256(json.dumps(original_data, sort_keys=True))

# Integritas returns proof tied to this hash

# Verification recalculates hash and compares
is_valid = sdk.verify_timestamp(record)
```

## API Key Security

### Storage Best Practices
**Never hardcode API keys in source code:**

❌ **INSECURE**:
```python
# Never do this
sdk = WearablesSDK(api_key="sk_live_12345...")
```

✅ **SECURE** approaches:

**1. Environment Variables**
```python
import os
sdk = WearablesSDK(api_key=os.environ["INTEGRITAS_API_KEY"])
```

**2. Platform Keychain/Keystore**
- **Android**: Android Keystore System
- **iOS**: Keychain Services
- **Tizen**: Secure Storage API

**3. Configuration Files (with proper permissions)**
```python
# config.json (chmod 600)
{
    "integritas_api_key": "your_key_here"
}
```

### Key Management
- Use separate keys for development and production
- Rotate keys regularly (Integritas supports multiple active keys)
- Monitor key usage and set up alerts for unusual activity
- Revoke compromised keys immediately

## Network Security

### Transport Layer Security
- All communication uses HTTPS/TLS 1.2+
- Certificate pinning recommended for production apps
- Automatic retry with exponential backoff for failed requests

### Data Minimization
- Only SHA3 hashes (not raw data) transmitted to Integritas
- Hashes are 64 characters (256 bits) - minimal bandwidth usage
- No personally identifiable information in transmitted data

### Privacy by Design
- Raw sensor data never leaves the device
- Integritas only receives cryptographic hashes
- Timestamp proofs contain no user data
- Local verification possible without network calls

## Threat Mitigation

### Replay Attacks
- Each data record includes unique ID with timestamp
- SHA3 hashing includes full context (sensor type, metadata, etc.)
- Integritas API validates hash format and rejects duplicates

### Man-in-the-Middle
- TLS encryption protects all network communication
- Certificate validation prevents MITM attacks
- Hash verification ensures data wasn't modified in transit

### Device Compromise
- API keys stored securely prevent unauthorized timestamping
- Local data integrity verification works even if network is compromised
- Queue-based processing limits impact of single-point failures

## Compliance Considerations

### GDPR/HIPAA Compliance
- **Data Minimization**: Only necessary data collected
- **Purpose Limitation**: Data used only for timestamping
- **Storage Limitation**: Raw data stays on device
- **Integrity and Confidentiality**: SHA3 hashing and TLS encryption

### Audit Trail
The SDK provides immutable audit trails through:
- Cryptographic proofs from Integritas blockchain
- Verifiable timestamps with nanosecond precision
- Tamper-evident data integrity checks
- Complete chain of custody for all sensor readings

## Security Testing

### Penetration Testing
Test these scenarios:
- API key exposure in memory dumps
- Network traffic analysis (should only show hashes)
- Device tampering attempts
- Queue overflow and denial-of-service

### Code Review Checklist
- [ ] API keys not hardcoded
- [ ] Proper error handling without information disclosure
- [ ] Input validation for sensor data
- [ ] Memory cleanup in shutdown procedures
- [ ] Thread safety in multi-threaded environments

### Monitoring and Alerting
Implement monitoring for:
- Unusual API key usage patterns
- High failure rates in timestamping
- Queue backlogs indicating resource exhaustion
- Verification failures indicating potential tampering

## Incident Response

### Key Compromise
1. Immediately revoke compromised API key in Integritas dashboard
2. Deploy new key through secure update mechanism
3. Audit all timestamped data created with compromised key
4. Notify affected users if required by regulations

### Data Tampering Detection
If `verify_timestamp()` returns False:
1. Isolate the affected data record
2. Check device integrity and security logs
3. Verify network connectivity and certificate validity
4. Contact Integritas support if systemic issue suspected

## Best Practices Summary

1. **Store API keys securely** using platform-specific secure storage
2. **Validate all input data** before recording
3. **Monitor system status** regularly using `get_status()`
4. **Implement proper error handling** for all SDK operations
5. **Test security assumptions** in your specific deployment environment
6. **Keep dependencies updated** to address security vulnerabilities
7. **Document your security model** for compliance and auditing
