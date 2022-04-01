# From https://github.com/FELToken/federated-learning-token/blob/main/felt/core/web3.py
from base64 import a85decode, a85encode
from nacl.public import Box, PrivateKey, PublicKey
import os
from pathlib import Path

def _hex_to_bytes(hex: str) -> bytes:
    return bytes.fromhex(hex[2:] if hex[:2] == "0x" else hex)

def export_public_key(private_key_hex: str) -> bytes:
    """Export public key for contract join request.
    Args:
        private_key: hex string representing private key
    Returns:
        32 bytes representing public key
    """
    return bytes(PrivateKey(_hex_to_bytes(private_key_hex)).public_key)

def encrypt_nacl(data: bytes) -> bytes:
    """Encryption function using NaCl box compatible with MetaMask
    For implementation used in MetaMask look into: https://github.com/MetaMask/eth-sig-util
    Args:
        public_key: public key of recipient
        data: message data
    Returns:
        encrypted data
    """
    public_key = export_public_key(os.environ.get("PRIVATE_KEY"))
    emph_key = PrivateKey.generate()
    enc_box = Box(emph_key, PublicKey(public_key))
    # Encryption is required to work with MetaMask decryption (requires utf8)
    data = a85encode(data)
    ciphertext = enc_box.encrypt(data)
    return bytes(emph_key.public_key) + ciphertext

def decrypt_nacl(data: bytes) -> bytes:
    """Decryption function using NaCl box compatible with MetaMask
    For implementation used in MetaMask look into: https://github.com/MetaMask/eth-sig-util
    Args:
        private_key: private key to decrypt with
        data: encrypted message data
    Returns:
        decrypted data
    """
    private_key_hex = os.environ.get("PRIVATE_KEY")
    private_key = bytes(PrivateKey(_hex_to_bytes(private_key_hex)))
    emph_key, ciphertext = data[:32], data[32:]
    box = Box(PrivateKey(private_key), PublicKey(emph_key))
    return a85decode(box.decrypt(ciphertext))

def encrypt_weights(path):
    path = Path(path)
    with open(path, "rb") as f:
        byte = f.read()
    encrypted_weights = encrypt_nacl(byte)
    # with open(f"{path.stem}.bin", "wb") as f:
    #     f.write(encrypted_weights)
    return encrypted_weights

def decrypt_weights(path):
    with open(path, "rb") as f:
        encrypted_weights = f.read()
    decrypted_weights = decrypt_nacl(encrypted_weights)
    # filename ='netG2.pth'
    # with open(filename, "wb") as output:
    #     output.write(decrypted_weights)
    return decrypted_weights