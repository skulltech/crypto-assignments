import numpy as np
from sympy import Matrix


chars = 'abcdefghijklmnopqrstuvwxyz'


def encrypt(message, k):
	bsize = k.shape[0]
	words = message.split(' ')
	lenwords = [len(word) for word in words]
	message = ''.join(words)
	if len(message) % bsize:
		message = message.ljust(((len(message) // bsize) + 1) * bsize, 'a')

	enc = np.array([chars.index(char) for char in message])
	cipher = ''
	for i in range(enc.shape[0] // bsize):
		block = enc[i * bsize: ((i+1) * bsize)]
		be = np.mod(k @ block, 26)
		be = ''.join([chars[i] for i in be])
		cipher = cipher + be

	ret = ''
	for lw in lenwords:
		ret = ret + cipher[:lw] + ' '
		cipher = cipher[lw:]
	return ret


def decrypt(cipher, k):
	bsize = k.shape[0]
	kinv = np.array(Matrix(k).inv_mod(26))
	words = cipher.split(' ')
	lenwords = [len(word) for word in words]
	cipher = ''.join(words)
	if len(cipher) % bsize:
		cipher = cipher.ljust(((len(cipher) // bsize) + 1) * bsize, 'a')

	enc = np.array([chars.index(char) for char in cipher])
	plain = ''
	for i in range(enc.shape[0] // bsize):
		block = enc[i * bsize: ((i+1) * bsize)]
		bd = np.mod(kinv @ block, 26)
		bd = ''.join([chars[i] for i in bd])
		plain = plain + bd

	ret = ''
	for lw in lenwords:
		ret = ret + plain[:lw] + ' '
		plain = plain[lw:]
	return ret


k = np.array([[22, 3], [9, 6]])
text = 'speaking of dreams in a figurative sense then slowly talking about its impact in the literal sense thewriter keeps stressing on one very important point that dreams have an important role to play inamerican politics after all a liberal society is formed on the basis of ones imagination these imaginationsare a result of ones free thoughts which can be related to dreams as dreaming provides a picture of thereal world uncovering things which otherwise might not have been pondered upon due to narrowed andlimited freedom of imagining it may seem reckless to consider the possibility of turning to dreams towork through the political conditions today but ignoring them altogether might even be more recklesssays the author'

print(text)
enc = encrypt(text, k)
print(enc)
dec = decrypt(enc, k)
print(dec)
