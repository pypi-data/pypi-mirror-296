# zscryptography

A simple encryption library using AES and PKCS7 padding.

## Installation

```bash
pip install zscryptography
```
## Usage
```xml
from encryption import encrypt, decrypt

# Define your key and plaintext
key = "thisisaverysecretkey1234"
plain_text = "Hello, World!"

# Encrypt the plaintext
encrypted_text = encrypt(plain_text, key)
print(f"Encrypted: {encrypted_text}")

# Decrypt the ciphertext
decrypted_text = decrypt(encrypted_text, key)
print(f"Decrypted: {decrypted_text}")
```