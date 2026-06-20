"""
Quantum text encoding + simple circuit example using PennyLane.

This module implements:
- encode_text_to_amplitudes(text) -> amplitudes for state preparation (small demo)
- make_encryption_circuit(amplitudes) -> pennylane circuit
"""

from typing import List
import pennylane as qml
import numpy as np

def encode_text_to_amplitudes(text: str, n_qubits: int = 3) -> np.ndarray:
    # Very small demo: convert bytes -> normalized amplitudes (truncate/pad)
    b = text.encode("utf-8")[: (2**n_qubits)]
    arr = np.frombuffer(b, dtype=np.uint8).astype(np.float64)
    if arr.size < 2**n_qubits:
        arr = np.pad(arr, (0, 2**n_qubits - arr.size))
    arr += 1e-6  # avoid zeros
    arr = arr / np.linalg.norm(arr)
    return arr

def make_encryption_circuit(amplitudes: np.ndarray):
    n_states = int(np.log2(len(amplitudes)))
    dev = qml.device("default.qubit", wires=n_states)

    @qml.qnode(dev)
    def circuit():
        qml.AmplitudeEmbedding(amplitudes, wires=range(n_states), normalize=True)
        # add some demonstrative gates — in a real algorithm you'd put encryption ops here
        for i in range(n_states):
            qml.RX(0.4 * (i + 1), wires=i)
        return qml.state()
    return circuit, dev
