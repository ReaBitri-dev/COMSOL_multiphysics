import click
import json
from .api import encrypt_text
import os

@click.group()
def cli():
    pass

@cli.command()
@click.option('--text', '-t', help='Plain text to encrypt', required=False)
@click.option('--infile', '-i', type=click.Path(exists=True), help='Path to a text file', required=False)
@click.option('--password', '-p', prompt=True, hide_input=True, confirmation_prompt=False)
@click.option('--hybrid', is_flag=True, help='Enable hybrid PQC KEM (simulated)')
def encrypt_text_cmd(text, infile, password, hybrid):
    if infile:
        with open(infile, 'r', encoding='utf-8') as fh:
            text = fh.read()
    elif not text:
        raise click.UsageError("Provide --text or --infile")

    res = encrypt_text(text, password, hybrid=hybrid)
    print("Ciphertext (base64):", res["ciphertext"][:80] + "...")
    print("Metadata saved to:", res["metadata_path"])
    print("Circuit (text preview):\n")
    print(res["quantum_visual"]["circuit"])

if __name__ == "__main__":
    cli()
