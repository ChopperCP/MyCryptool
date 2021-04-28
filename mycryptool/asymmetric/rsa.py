from ..tools import *


def encrypt(plaintext: bytes, public_key: 'Tuple (e, n)'):
	e, n = public_key
	m = bytes2int(plaintext)
	if m >= n:
		raise Exception("Plain text too long")
	return int2bytes(quick_power(m, e, n))


def decrypt(ciphertext: bytes, private_key: 'Tuple (d, n)'):
	d, n = private_key
	c = bytes2int(ciphertext)
	if c >= n:
		raise Exception("Cipher text too long")
	return int2bytes(quick_power(c, d, n))


def generate_key_pair():
	"""
	Randomly generate a RSA key pair
	Returns ( public key, private key )
	"""
	p = generate_prime(2048)
	q = generate_prime(2048)
	n = p * q
	e = 65537  # 65537 is prime.

	phi = (p - 1) * (q - 1)
	d = invert(e, phi)
	return (e, n), (d, n)


def get_signature(data_hash: bytes, private_key: 'Tuple (d, n)'):
	return encrypt(data_hash, private_key)


def is_valid_signature(data_hash: bytes, signature, public_key: 'Tuple (e, n)'):
	if data_hash == decrypt(signature, public_key):
		return True
	return False
