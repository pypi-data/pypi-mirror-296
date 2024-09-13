# -*- encoding: utf-8 -*-
"""
kerkle.helping module

"""
import hashlib

import blake3
from keri import core
from keri.core import MtrDex
from keri.core.coring import Digestage

LEAF = b"\x00"
NODE = b"\x01"
KEYSIZE = 32
DEPTH = KEYSIZE * 8

RIGHT = 1
PLACEHOLDER = bytes(32)
DEFAULTVALUE = b""

Digests = {
    MtrDex.Blake3_256: Digestage(klas=blake3.blake3, size=None, length=None),
    MtrDex.Blake2b_256: Digestage(klas=hashlib.blake2b, size=32, length=None),
    MtrDex.Blake2s_256: Digestage(klas=hashlib.blake2s, size=None, length=None),
    MtrDex.SHA3_256: Digestage(klas=hashlib.sha3_256, size=None, length=None),
    MtrDex.SHA2_256: Digestage(klas=hashlib.sha256, size=None, length=None),
    MtrDex.Blake3_512: Digestage(klas=blake3.blake3, size=None, length=64),
    MtrDex.Blake2b_512: Digestage(klas=hashlib.blake2b, size=None, length=None),
    MtrDex.SHA3_512: Digestage(klas=hashlib.sha3_512, size=None, length=None),
    MtrDex.SHA2_512: Digestage(klas=hashlib.sha512, size=None, length=None),
}


def create_leaf(path, code=core.MtrDex.SHA3_256):
    value = b"".join([LEAF, path])
    dig = digest(value, code=code)
    return dig, value


def parse_leaf(data):
    return data[1:33]


def is_leaf(data):
    return data[0] == 0


def create_node(left, right, code=core.MtrDex.SHA3_256):
    value = b"".join([NODE, left, right])
    dig = digest(value, code=code)
    return dig, value


def parse_node(data):
    return data[1:33], data[33:]


def digest(data, code=core.MtrDex.Blake3_256):
    # we have to create a new instance has hashlib doesn't
    # have a 'reset' for updates
    if code not in core.DigDex:
        raise ValueError("Unsupported digest code = {}.".format(code))

    # string now has
    # correct size
    klas, size, length = Digests[code]
    # sad as 'v' verision string then use its kind otherwise passed in kind
    ckwa = dict()  # class keyword args
    if size:
        ckwa.update(digest_size=size)  # optional digest_size
    dkwa = dict()  # digest keyword args
    if length:
        dkwa.update(length=length)
    cpa = [data]
    return klas(*cpa, **ckwa).digest(**dkwa)


def get_bit(index, data):
    if data[index >> 3] & 1 << (7 - index % 8) > 0:
        return 1
    else:
        return 0


def count_set_bits(data):
    count = 0
    for i in range(0, len(data) * 8):
        if get_bit(i, data) == 1:
            count += 1
    return count


def count_common_prefix(a, b):
    count = 0
    for i in range(0, len(a) * 8):
        if get_bit(i, a) == get_bit(i, b):
            count += 1
        else:
            return count
    return count


# lil helper
def show_bits(value):
    x = [bin(byte) for byte in value]
    return "{}".format(x)


def big_test(tree, size):
    import secrets

    for i in range(size):
        k = secrets.token_bytes(10)
        v = bytes("hello{}".format(i), "utf-8")
        tree.update(k, v)
