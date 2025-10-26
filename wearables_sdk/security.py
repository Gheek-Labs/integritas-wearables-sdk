# wearables_sdk/security.py
"""Security utilities for API key loading, JSON validation, and optional TLS pinning."""
import os, json, ssl, socket, hashlib
from typing import Optional, List

def load_api_key(env_var: str = "INTEGRITAS_API_KEY", fallback_file: Optional[str] = None) -> str:
    """Load API key from environment or a restricted-permission file.
    Raises ValueError if not found.
    """
    key = os.environ.get(env_var)
    if key:
        return key.strip()
    if fallback_file and os.path.exists(fallback_file):
        with open(fallback_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if content:
                return content
    raise ValueError("API key not found. Set env INTEGRITAS_API_KEY or provide fallback_file.")

def ensure_json_compact(obj) -> str:
    """Dump JSON with sorted keys, no whitespace, and forbid NaN/Infinity."""
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False)

def sha256_cert_fingerprint(hostname: str, port: int = 443) -> str:
    """Fetch peer certificate and return SHA-256 fingerprint as colon-delimited hex."""
    ctx = ssl.create_default_context()
    with socket.create_connection((hostname, port)) as sock:
        with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
            der_cert = ssock.getpeercert(binary_form=True)
    fp = hashlib.sha256(der_cert).hexdigest().upper()
    return ':'.join(fp[i:i+2] for i in range(0, len(fp), 2))

def matches_any_fingerprint(actual_fp: str, allowed: List[str]) -> bool:
    """Compare actual fingerprint against allowed list (case-insensitive)."""
    af = actual_fp.replace('-', ':').upper()
    normalized = [a.replace('-', ':').upper() for a in allowed]
    return af in normalized
