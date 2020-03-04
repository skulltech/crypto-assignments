from genkeys import generate_keys
import client
from gmpy2 import mpz
import random
import string

klen = 100
bit_length = 256

na, pka, ska = generate_keys(bit_length)
nb, pkb, skb = generate_keys(bit_length)
k = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(klen))
print('[*] Symmetric key:', k)
message = input('[*] Enter your message: ')

ret = client.encrypt(message, k, nb, pkb, na, ska)
print('-'*20)
print('[*] Encrypted message:', ret[0])
print('[*] Encrypted key:', ret[1])

ret = client.decrypt(ret[0], ret[1], na, pka, nb, skb)
print('-'*20)
print('[*] Recovered message:', ret[0])
print('[*] Recovered key:', ret[1])
