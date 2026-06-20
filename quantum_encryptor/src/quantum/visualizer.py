from typing import Tuple
import pennylane as qml
import numpy as np

def show_state_and_circuit(circuit_func, dev):
    # circuit_func is the qnode; dev is the pennylane device
    state = circuit_func()
    # circuit drawing (text)
    circ_txt = circuit_func.draw(output="text")
    return {"statevector": np.array(state).tolist(), "circuit": str(circ_txt)}
