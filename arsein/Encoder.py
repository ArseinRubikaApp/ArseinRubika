import base64
import io
import json
import random
import re
import secrets
import string
from base64 import b64decode
from json import JSONDecoder, loads

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Util.Padding import pad, unpad

from .Error import AuthError


class encoderjson:
    def __init__(self, auth: str, private_key: str = None):
        self.auth = auth
        self.key = bytearray(self.createSecretPassphrase(auth), "UTF-8")
        self.iv = bytearray.fromhex("0" * 32)
        if private_key:
            self.keypair = RSA.import_key(private_key.encode("utf-8"))

    def changeAuthType(auth):
        auth = auth.encode()
        input_chars = b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        output_chars = b"gfedcbazyxwvutsrqponmlkjihDCBAZYXWVUTSRQPONMLKJIHGFE3210987654"
        trans = bytes.maketrans(input_chars, output_chars)
        return auth.translate(trans).decode()

    def createSecretPassphrase(self,auth):
        auth = auth.encode()
        auth = auth[16:24] + auth[0:8] + auth[24:32] + auth[8:16]
        input_chars = b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
        output_chars = b'jklmnopqrstuvwxyzabcdefghidefghijklmnopqrstuvwxyzabc5678901234'
        trans = bytes.maketrans(input_chars, output_chars)
        return auth.translate(trans).decode()

    def encrypt(self, text):
        try:
            encode_data = base64.b64encode(
                AES.new(self.key, AES.MODE_CBC, self.iv).encrypt(
                    pad(text.encode("UTF-8"), AES.block_size)
                )
            ).decode("UTF-8")
            return encode_data
        except:
            raise

    def decrypt(self, text):
        try:
            decode_data = unpad(
                AES.new(self.key, AES.MODE_CBC, self.iv).decrypt(
                    base64.urlsafe_b64decode(text.encode("UTF-8"))
                ),
                AES.block_size,
            ).decode("UTF-8")
            return decode_data
        except ValueError:
            raise AuthError(
                "Check your auth This auth is not the key to decrypt and encrypt data"
            )

    def makeSignFromData(self, data_enc: str):
        sha_data = SHA256.new(data_enc.encode("utf-8"))
        signature = pkcs1_15.new(self.keypair).sign(sha_data)
        return base64.b64encode(signature).decode("utf-8")

    def decryptRsaOaep(private: str, data_enc: str):
        keyPair = RSA.import_key(private.encode("utf-8"))
        return (
            PKCS1_OAEP.new(keyPair).decrypt(base64.b64decode(data_enc)).decode("utf-8")
        )

    def encryptRsaOaep(private: str, data_enc: str):
        keyPair = RSA.import_key(private.encode("utf-8"))
        return (
            PKCS1_OAEP.new(keyPair).encrypt(base64.b64encode(data_enc)).decode("utf-8")
        )

    def rsaKeyGenerate():
        keyPair = RSA.generate(1024)
        public = encoderjson.changeAuthType(
            base64.b64encode(keyPair.publickey().export_key()).decode("utf-8")
        )
        private = keyPair.export_key().decode("utf-8")
        return [public, private]


def getThumbInline(image_bytes: bytes):
    import base64
    from PIL import Image

    try:
        resample = Image.Resampling.LANCZOS
    except AttributeError:
        resample = Image.ANTIALIAS

    im = Image.open(io.BytesIO(image_bytes))
    width, height = im.size

    if height > width:
        new_height = 40
        new_width = round(new_height * width / height)
    else:
        new_width = 40
        new_height = round(new_width * height / width)

    im = im.resize((new_width, new_height), resample)

    buffer = io.BytesIO()
    im.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue())
