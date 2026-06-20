import json
import os
from typing import Dict, Any
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
import base64

META_DIR = os.path.join(os.path.dirname(__file__), "..", "metadata_store")
os.makedirs(META_DIR, exist_ok=True)

# --- symmetric helpers (AES-GCM wrapper) ----------------
def derive_key(password: str, salt: bytes = None, iterations: int = 200_000) -> (bytes, bytes):
    if salt is None:
        salt = get_random_bytes(16)
    key = PBKDF2(password, salt, dkLen=32, count=iterations)
    return key, salt

def aes_encrypt(data: bytes, key: bytes) -> Dict[str, bytes]:
    nonce = get_random_bytes(12)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(data)
    return {"nonce": nonce, "tag": tag, "ciphertext": ct}

def aes_decrypt(enc: Dict[str, bytes], key: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_GCM, nonce=enc["nonce"])
    return cipher.decrypt_and_verify(enc["ciphertext"], enc["tag"])

# --- metadata storage (encrypted using Fernet) ----------
# Fernet key should be kept safe; for demo we derive from password
def make_fernet_key_from_password(password: str, salt: bytes) -> bytes:
    # returns a 32 url-safe base64 key for Fernet
    key, _ = derive_key(password, salt)
    return base64.urlsafe_b64encode(key)

def save_encrypted_metadata(filename: str, metadata: Dict[str, Any], password: str):
    meta_path = os.path.join(META_DIR, filename)
    salt = get_random_bytes(16)
    fernet_key = make_fernet_key_from_password(password, salt)
    f = Fernet(fernet_key)
    payload = json.dumps(metadata, default=str).encode("utf-8")
    token = f.encrypt(payload)
    with open(meta_path, "wb") as fh:
        fh.write(salt + token)  # prefix salt for retrieval
    return meta_path

def load_encrypted_metadata(path: str, password: str) -> Dict[str, Any]:
    with open(path, "rb") as fh:
        raw = fh.read()
    salt, token = raw[:16], raw[16:]
    fernet_key = make_fernet_key_from_password(password, salt)
    f = Fernet(fernet_key)
    payload = f.decrypt(token)
    return json.loads(payload.decode("utf-8"))
