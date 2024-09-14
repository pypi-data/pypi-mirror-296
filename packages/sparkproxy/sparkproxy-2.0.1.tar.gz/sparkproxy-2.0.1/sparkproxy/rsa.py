# coding=utf-8
from __future__ import absolute_import, division, print_function
from sparkproxy.util import to_bytes, to_hex, from_hex

# 尝试导入Python 3中的库，如果失败，则回退到Python 2的等效库

try:
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding
except ImportError:
    # Python 2的兼容代码，或其他回退代码
    # 注意：cryptography库在Python 2和Python 3中的用法相同，所以这里主要是演示结构
    pass


def rsa_load_pem_private_key(pri_key):
    private_key = serialization.load_pem_private_key(
        pri_key,
        password=None,
        backend=default_backend()
    )
    return private_key


def rsa_load_pem_public_key(pub_key):
    public_key = serialization.load_pem_public_key(
        pub_key,
        backend=default_backend()
    )
    return public_key


def rsa_public_encrypt(msg, public_key):
    decoded_msg = to_bytes(msg)

    encrypted_msg = public_key.encrypt(
        decoded_msg,
        padding.PKCS1v15()
    )

    return to_hex(encrypted_msg)


def rsa_private_decrypt(encrypted_msg_hex, private_key):
    encrypted_msg = from_hex(encrypted_msg_hex)

    decrypted_msg = private_key.decrypt(
        encrypted_msg,
        padding.PKCS1v15()
    )

    return decrypted_msg


def rsa_sign(message, private_key):
    signature = private_key.sign(
        to_bytes(message),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return to_hex(signature)


def rsa_verify(sign, message, public_key):
    try:
        decoded_sign = from_hex(sign)
    except Exception as e:
        raise ValueError("签名解码失败: {}".format(e))

    public_key.verify(
        decoded_sign,
        to_bytes(message),
        padding.PKCS1v15(),
        hashes.SHA256()
    )