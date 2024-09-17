import os
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def encrypt(plain_text, key, iv=None):
    if not key:
        raise ValueError("Key must be provided")
    
    if not iv:
        iv = os.urandom(16)
    
    cipher = Cipher(algorithms.AES(key.encode('utf-8')), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_data = padder.update(plain_text.encode('utf-8')) + padder.finalize()
    
    cipher_bytes = encryptor.update(padded_data) + encryptor.finalize()
    
    return b64encode(iv + cipher_bytes).decode('utf-8')

def decrypt(cipher_text, key, iv=None):
    if not key:
        raise ValueError("Key must be provided")
    
    cipher_data = b64decode(cipher_text)
    
    if not iv:
        iv = cipher_data[:16]
        cipher_data = cipher_data[16:]
    else:
        iv = iv.encode('utf-8')
    
    cipher = Cipher(algorithms.AES(key.encode('utf-8')), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    plain_bytes = decryptor.update(cipher_data) + decryptor.finalize()
    
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    plain_bytes = unpadder.update(plain_bytes) + unpadder.finalize()
    
    return plain_bytes.decode('utf-8')