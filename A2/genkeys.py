import gmpy2
from gmpy2 import mpz
import time
import random
import string

rand_state = gmpy2.random_state(int(time.time() * 100000))
klen = 8

def generate_prime(bits):
    temp = gmpy2.mpz_rrandomb(rand_state, bits)
    return gmpy2.next_prime(temp)

def generate_keys(bits):
    while True:
        p = generate_prime(bits)
        q = generate_prime(bits)
        if p != q:
            break

    n = gmpy2.mul(p, q)
    phi = gmpy2.mul(p-1, q-1)

    while True:
        e = gmpy2.mpz_random(rand_state, phi)
        if e > 1 and gmpy2.gcd(e, phi) == 1:
            break

    d = gmpy2.invert(e, phi)
    return n, e, d


def main():
    n, e, d = generate_keys(64)
    print('[*] N:         ', n)
    print('[*] Public Key:', e)
    print('[*] Secret Key:', d)
    print('[*] Symmtr Key:', ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(klen)))


if __name__ == '__main__':
    main()
