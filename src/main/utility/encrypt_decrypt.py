import base64
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
import os, sys
from resources.dev import config
# from logging_config import logger

try:
    key = config.key
    iv = config.iv
    salt = config.salt

    if not (key and iv and salt):
        raise Exception(F"Error while fetching details for key/iv/salt")
except Exception as e:
    print(f"Error occured. Details : {e}")
    # logger.error("Error occurred. Details: %s", e)
    sys.exit(0)

BS = 16
pad = lambda s: bytes(s + (BS - len(s) % BS) * chr(BS - len(s) % BS), 'utf-8')
unpad = lambda s: s[0:-ord(s[-1:])]

def get_private_key():
    Salt = salt.encode('utf-8')
    kdf = PBKDF2(key, Salt, 64, 1000)
    key32 = kdf[:32]
    return key32

def encrypt(raw):
    raw = pad(raw)
    cipher = AES.new(get_private_key(), AES.MODE_CBC, iv.encode('utf-8'))
    return base64.b64encode(cipher.encrypt(raw))

def decrypt(enc):
    padded_enc = enc + '=' * (-len(enc) % 4)
    decoded_enc = base64.b64decode(padded_enc)
    # cipher = AES.new(get_private_key(), AES.MODE_CBC, iv.encode('utf-8'))
    cipher = AES.new(get_private_key(), AES.MODE_CBC, iv.encode('utf-8'))
    decrypted_data = unpad(cipher.decrypt(decoded_enc), AES.block_size).decode('utf-8')
    return decrypted_data
