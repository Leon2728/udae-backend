"""Hash utilities for deterministic identity.

All hashing is SHA-256 to ensure cryptographic stability and auditability.
No randomness, no timestamps, no non-deterministic behavior.
"""

import hashlib
import json
from typing import Any


def hash_bytes(data: bytes) -> str:
    """Compute SHA-256 hash of bytes.
    
    Args:
        data: Raw bytes to hash.
        
    Returns:
        Hex string representation of SHA-256 hash.
    """
    return hashlib.sha256(data).hexdigest()


def hash_json(obj: Any) -> str:
    """Compute SHA-256 hash of JSON-serializable object.
    
    Args:
        obj: Any JSON-serializable Python object.
        
    Returns:
        Hex string representation of SHA-256 hash.
        
    Note:
        Deterministic: uses sort_keys=True for consistent ordering.
    """
    json_str = json.dumps(obj, sort_keys=True, separators=(',', ':'))
    return hash_bytes(json_str.encode('utf-8'))


def hash_string(text: str) -> str:
    """Compute SHA-256 hash of string.
    
    Args:
        text: String to hash.
        
    Returns:
        Hex string representation of SHA-256 hash.
    """
    return hash_bytes(text.encode('utf-8'))
