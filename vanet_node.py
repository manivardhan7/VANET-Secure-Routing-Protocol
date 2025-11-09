# utils.py
import json
import time
import os
import hmac
import hashlib
import hmac
from typing import Dict, Any

# Optional RSA (requires cryptography)
try:
    from cryptography.hazmat.primitives import hashes, serialization
    from cryptography.hazmat.primitives.asymmetric import padding, rsa
    RSA_AVAILABLE = True
except Exception:
    RSA_AVAILABLE = False

# Shared secret for HMAC (in real deployment use secure K management)
SHARED_SECRET = os.environ.get("VANET_SHARED_SECRET", "supersecret_shared_key").encode()

def current_millis() -> int:
    return int(time.time() * 1000)

def make_message(sender_id: str, position: Dict[str, float], payload: Dict[str, Any], use_nonce=True) -> Dict[str, Any]:
    """
    Compose the message dict (before signing/hmac).
    """
    msg = {
        "sender": sender_id,
        "timestamp": current_millis(),
        "position": position,
        "payload": payload
    }
    if use_nonce:
        # simple nonce using timestamp + random bits
        msg["nonce"] = str(msg["timestamp"]) + "_" + hashlib.sha1((sender_id + str(msg["timestamp"])).encode()).hexdigest()[:8]
    return msg

def serialize_message(msg: Dict[str, Any]) -> bytes:
    """
    Stable JSON serialization for HMAC/signature.
    """
    return json.dumps(msg, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()

def hmac_sign(msg: Dict[str, Any], key: bytes = SHARED_SECRET) -> str:
    b = serialize_message(msg)
    mac = hmac.new(key, b, hashlib.sha256).hexdigest()
    return mac

def hmac_verify(msg: Dict[str, Any], mac_hex: str, key: bytes = SHARED_SECRET) -> bool:
    expected = hmac_sign(msg, key)
    # Use hmac.compare_digest for constant-time comparison
    return hmac.compare_digest(expected, mac_hex)

# Optional RSA signing and verifying (only if cryptography installed)
def generate_rsa_keys():
    if not RSA_AVAILABLE:
        raise RuntimeError("cryptography not installed.")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key

def rsa_sign(msg: Dict[str, Any], private_key) -> bytes:
    b = serialize_message(msg)
    return private_key.sign(
        b,
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256(),
    )

def rsa_verify(msg: Dict[str, Any], signature: bytes, public_key) -> bool:
    b = serialize_message(msg)
    try:
        public_key.verify(
            signature,
            b,
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256(),
        )
        return True
    except Exception:
        return False
