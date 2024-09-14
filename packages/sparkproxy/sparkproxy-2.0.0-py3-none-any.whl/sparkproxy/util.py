# coding=utf-8
import binascii
import sys


def to_bytes(data, encoding='utf-8'):
    """确保s是字节类型"""
    if sys.version_info[0] < 3:
        # Python 2.x，s已经是字节串
        return data
    else:
        # Python 3.x，确保是bytes
        return data.encode(encoding) if isinstance(data, str) else data


def to_string(data, encoding='utf-8'):
    """
    将数据转换为字符串。

    Args:
        data: 要转换的数据。
        encoding: 字符串编码。

    Returns:
        str: 转换后的字符串。
    """
    if isinstance(data, bytes):
        return data.decode(encoding)
    elif isinstance(data, str):
        return data
    else:
        return str(data)


# 兼容Python 2和3的十六进制解码函数
def from_hex(s):
    try:
        return bytes.fromhex(s)  # Python 3
    except AttributeError:
        return s.decode('hex')  # Python 2


# 兼容Python 2和3的十六进制编码函数
def to_hex(data):
    try:
        return data.hex()  # Python 3
    except AttributeError:
        return binascii.hexlify(data)  # Python 2