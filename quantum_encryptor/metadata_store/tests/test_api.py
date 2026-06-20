from src.api import encrypt_text
import pytest

def test_encrypt_text_basic():
    res = encrypt_text("hi", "testpassword", hybrid=False)
    assert "ciphertext" in res
    assert "metadata_path" in res
    assert "quantum_visual" in res
