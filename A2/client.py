import argparse
import gmpy2
from gmpy2 import mpz
from genkeys import klen

chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def encode(string):
    code = mpz(0)
    for i, c in enumerate(string):
        code = code + (chars.index(c) * (len(chars) ** i))
    return code

def decode(code):
    string = []
    blen = 0
    while (len(chars) ** blen) < code:
        blen = blen + 1
    for i in range(blen):
        string.append(chars[code % len(chars)])
        code = code // len(chars)
    return ''.join(string)

def vignere_decrypt(cipher, key):
    key = [chars.index(c) for c in key]
    plain = []
    for i, c in enumerate(cipher):
        plain.append(chars[(chars.index(c) - key[i % len(key)]) % 26])
    return ''.join(plain)

def vignere_encrypt(plain, key):
    key = [chars.index(c) for c in key]
    cipher = []
    for i, c in enumerate(plain):
        cipher.append(chars[(chars.index(c) + key[i % len(key)]) % 26])
    return ''.join(cipher)


def encrypt(m, k, pn, pk, sn, sk):
    c = vignere_encrypt(m, k)
    key_int = encode(k)
    kd = gmpy2.powmod(key_int, sk, sn)
    kd = decode(gmpy2.powmod(kd, pk, pn))
    return c, kd

def decrypt(c, kd, pn, pk, sn, sk):
    k = gmpy2.powmod(encode(kd), sk, sn)
    k = int(gmpy2.powmod(k, pk, pn))
    key_string = decode(k)
    m = vignere_decrypt(c, key_string)
    return m, key_string


def rsa_encrypt(plain, n1, key1, bsize):
    residual = len(plain) % bsize
    if residual:
        plain = plain + 'X' * (bsize - residual)
    cipher = ''
    for i in range(len(plain) // bsize):
        block = plain[i*bsize: (i+1)*bsize]
        block_int = encode(block)
        enc = gmpy2.powmod(block_int, key1, n1)
        cipher = cipher + decode(int(enc))
    return cipher
