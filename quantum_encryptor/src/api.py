"""
Unified API: encrypt_text, encrypt_audio, encrypt_image, encrypt_file, encrypt_video
For now, audio/image/video are stubs that call file-level handlers.
"""

import os
import json
from typing import Tuple, Dict, Any
from .utils import derive_key, aes_encrypt, aes_decrypt, save_encrypted_metadata
from .pqc import kem_generate_keypair, kem_encapsulate
from .quantum.text_quantum import encode_text_to_amplitudes, make_encryption_circuit
from .quantum.visualizer import show_state_and_circuit
import base64

# Example encryption function for text
def encrypt_text(plaintext: str, password: str, hybrid: bool = False) -> Dict[str, Any]:
    # 1) derive symmetric key from password
    key, salt = derive_key(password)
    # 2) optional hybrid PQC KEM
    pqc_meta = {}
    if hybrid:
        pk, sk = kem_generate_keypair()
        enc = kem_encapsulate(pk)
        shared = enc["shared_key"]
        # combine derived key and shared (XOR for demo)
        key = bytes(a ^ b for a, b in zip(key, shared[:len(key)]))
        pqc_meta = {"capsule": base64.b64encode(enc["capsule"]).decode("ascii"), "pk": base64.b64encode(pk).decode("ascii")}

    # 3) quantum encoding (demo)
    amplitudes = encode_text_to_amplitudes(plaintext, n_qubits=3)
    circuit, dev = make_encryption_circuit(amplitudes)
    qstate_info = show_state_and_circuit(circuit, dev)

    # 4) symmetric encrypt original plaintext for output
    enc = aes_encrypt(plaintext.encode("utf-8"), key)

    metadata = {
        "algorithm": "demo-quantum+AES-GCM",
        "salt": base64.b64encode(salt).decode("ascii"),
        "pqc_meta": pqc_meta,
        "quantum": {"n_qubits": int(np.log2(len(amplitudes))), "statevector_len": len(amplitudes)}
    }

    # save encrypted metadata to file (password-protect)
    meta_path = save_encrypted_metadata("last_metadata.bin", metadata, password)

    result = {
        "ciphertext": base64.b64encode(enc["ciphertext"]).decode("ascii"),
        "nonce": base64.b64encode(enc["nonce"]).decode("ascii"),
        "tag": base64.b64encode(enc["tag"]).decode("ascii"),
        "metadata_path": meta_path,
        "quantum_visual": qstate_info
    }
    return result

# small compatibility helper for numpy import in metadata
import numpy as np
