import streamlit as st
from src.api import encrypt_text
import json
import base64

st.set_page_config(page_title="Quantum Encryptor (Demo)", layout="centered")

st.title("Quantum Encryptor — Demo")
st.write("Small demonstration: text encryption with PennyLane visualization (statevector + circuit).")

with st.form("enc_form"):
    text = st.text_area("Text to encrypt", value="Hello world")
    password = st.text_input("Password (used to derive symmetric key)", type="password")
    hybrid = st.checkbox("Enable hybrid PQC (simulated)")
    submitted = st.form_submit_button("Encrypt")

if submitted:
    if not password:
        st.error("Provide a password.")
    else:
        res = encrypt_text(text, password, hybrid=hybrid)
        st.success("Encrypted!")
        st.subheader("Ciphertext (base64, truncated)")
        st.code(res["ciphertext"][:200] + "...")
        st.subheader("Circuit")
        st.text(res["quantum_visual"]["circuit"])
        st.subheader("Statevector (first 8 entries)")
        st.write(res["quantum_visual"]["statevector"][:8])
        st.subheader("Metadata path")
        st.write(res["metadata_path"])
