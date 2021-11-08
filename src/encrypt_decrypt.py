import base64
from typing import Any
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Protocol.KDF import PBKDF2
 
BLOCK_SIZE = 16
pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * chr(BLOCK_SIZE - len(s) % BLOCK_SIZE)
unpad = lambda s: s[:-ord(s[len(s) - 1:])]

SECRET_KEY = 'secret key'  # Keep it secret in production use
 

def get_private_key(secret_key: str) -> bytes:
    salt = b"this is a salt"
    kdf = PBKDF2(secret_key, salt, 64, 1000)
    key = kdf[:32]
    return key
 
 
def encrypt(raw: str, secret_key: str) -> bytes:
    private_key = get_private_key(secret_key)
    raw = pad(raw).encode("UTF-8")
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw))
 
 
def decrypt(enc: bytes, secret_key: str) -> Any:
    private_key = get_private_key(secret_key)
    enc = base64.b64decode(enc)
    iv = enc[:16]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[16:]))
 

msg = input("Enter message: ")

# First let us encrypt secret message
encrypted = encrypt(msg, SECRET_KEY)
print(encrypted)
 
# Let us decrypt using our original secret_key
decrypted = decrypt(encrypted, SECRET_KEY)
print(bytes.decode(decrypted))
