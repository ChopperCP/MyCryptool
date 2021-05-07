'''
Equivalent code to sha1.py
WARNING:
	FOR STUDY ONLY
	TOO SLOW FOR ANY PROGRAMMING USE
'''

from bitarray import bitarray
from bitarray.util import int2ba, ba2int

# Buffers
H0 = int2ba(0x67452301, endian='big', length=32)
H1 = int2ba(0xEFCDAB89, endian='big', length=32)
H2 = int2ba(0x98BADCFE, endian='big', length=32)
H3 = int2ba(0x10325476, endian='big', length=32)
H4 = int2ba(0xC3D2E1F0, endian='big', length=32)

W = []


def _padding(data: bitarray):
	if len(data) % 512 >= 448:
		padding_len = 512 - (len(data) - 448)
	else:
		padding_len = 448 - len(data)

	# Append the length of data as well.
	data_len_encoded = int2ba(len(data), endian='big', length=64)
	return data + bitarray('1' + '0' * (padding_len - 1)) + data_len_encoded


def _round(block: bitarray):
	global W
	global H0, H1, H2, H3, H4
	mod = 1 << 32

	def cir_left_shift(data: bitarray, n: int):
		return (data << n) | (data >> len(data) - n)

	def word_add(*args):
		# Returns int(lhs)+int(rhs) % 2**32
		ans = 0
		for arg in args:
			ans = (ans + ba2int(arg)) % mod
		return int2ba(ans)

	A = H0[:]
	B = H1[:]
	C = H2[:]
	D = H3[:]
	E = H4[:]

	def K(t: 'int>0'):
		# Constant words
		if t <= 19:
			return bitarray(0x5A827999, endian='big')
		elif 40 > t >= 20:
			return bitarray(0x6ED9EBA1, endian='big')
		elif 60 > t >= 40:
			return bitarray(0x8F1BBCDC, endian='big')
		else:
			return bitarray(0xCA62C1D6, endian='big')

	def f(t: 'int>0'):
		if t <= 19:
			return (B & C) | ((~B) & D)
		elif 40 > t >= 20:
			return B ^ C ^ D
		elif 60 > t >= 40:
			return (B & C) | (B & D) | (C & D)
		else:
			return B ^ C ^ D

	# Initialize W

	for t in range(16):
		W.append(block[32 * t:32 * (t + 1)])

	for t in range(16, 80):
		W.append(cir_left_shift(
			W[t - 3] ^ W[t - 8] ^ W[t - 14] ^ W[t - 16], 1))

	# Main  round loop
	for t in range(80):
		temp = word_add(cir_left_shift(A, 5), f(t), E, W[t], K(t))
		E = D
		D = C
		C = cir_left_shift(B, 30)
		B = A
		A = temp

	H0 = word_add(H0, A)
	H1 = word_add(H1, B)
	H2 = word_add(H2, C)
	H3 = word_add(H3, D)
	H4 = word_add(H4, E)


def sha1(data: bytes):
	data_arr = bitarray(endian='big')
	data_arr.frombytes(data)
	data = data_arr

	data = _padding(data)
	for i in range(0, len(data), 512):
		# For each block
		block = data[i:i + 512]
		_round(block)

	return (H0 + H1 + H2 + H3 + H4).tobytes()


print(sha1(b'Jessie Pinkman in the house!'))
