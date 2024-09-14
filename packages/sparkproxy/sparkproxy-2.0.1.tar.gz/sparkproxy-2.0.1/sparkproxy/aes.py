# coding=utf-8
from __future__ import absolute_import, division, print_function

import base64
import json

from sparkproxy.util import to_bytes, to_string

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import padding
except ImportError:
    # Python 2的兼容代码，或其他回退代码
    # 注意：cryptography库在Python 2和Python 3中的用法相同，所以这里主要是演示结构
    pass


def pkcs5_padding(data, block_size):
    if isinstance(data, str):
        data = data.encode('utf-8')

    padder = padding.PKCS7(block_size * 8).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data


def pkcs5_unpadding(padded_data, block_size):
    unpadder = padding.PKCS7(block_size * 8).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data


def aes_encrypt_cbc(orig_data, key):
    # Ensure key length is 16, 24, or 32 bytes
    assert len(key) in [16, 24, 32], "Key length must be 16, 24, or 32 bytes"

    block_size = 16
    orig_data = pkcs5_padding(orig_data, block_size)

    cipher = Cipher(algorithms.AES(key), modes.CBC(key[:block_size]), backend=default_backend())
    encryptor = cipher.encryptor()

    encrypted = encryptor.update(orig_data) + encryptor.finalize()
    return encrypted


def aes_decrypt_cbc(encrypted_data, key):
    # Ensure key length is 16, 24, or 32 bytes
    assert len(key) in [16, 24, 32], "Key length must be 16, 24, or 32 bytes"

    block_size = 16

    cipher = Cipher(algorithms.AES(key), modes.CBC(key[:block_size]), backend=default_backend())
    decryptor = cipher.decryptor()

    decrypted = decryptor.update(encrypted_data) + decryptor.finalize()
    decrypted = pkcs5_unpadding(decrypted, block_size)
    return decrypted


def encrypt_data(req, key):
    # JSON encode the request
    json_data = json.dumps(req)

    # AES encrypt the JSON data
    encrypted_data = aes_encrypt_cbc(json_data, key)

    # Base64 encode the encrypted data
    base64_encoded_data = to_string(base64.b64encode(encrypted_data))

    return base64_encoded_data


def decrypt_data(encrypted_request, key):
    # Base64 decode the encrypted data
    encrypted_data = base64.b64decode(to_bytes(encrypted_request))

    # AES decrypt the data
    decrypted_data = aes_decrypt_cbc(encrypted_data, key)

    # JSON decode the decrypted data
    return json.loads(decrypted_data)