import struct
from typing import List
from mycryptool.tools import xor_bytes

from bitarray import bitarray
from bitarray.util import ba2int
from bitarray.util import int2ba

INITIAL_PERMUTATION = (
	57, 49, 41, 33, 25, 17, 9, 1,
	59, 51, 43, 35, 27, 19, 11, 3,
	61, 53, 45, 37, 29, 21, 13, 5,
	63, 55, 47, 39, 31, 23, 15, 7,
	56, 48, 40, 32, 24, 16, 8, 0,
	58, 50, 42, 34, 26, 18, 10, 2,
	60, 52, 44, 36, 28, 20, 12, 4,
	62, 54, 46, 38, 30, 22, 14, 6,
)

INVERSE_INITIAL_PERMUTATION = (
	39, 7, 47, 15, 55, 23, 63, 31,
	38, 6, 46, 14, 54, 22, 62, 30,
	37, 5, 45, 13, 53, 21, 61, 29,
	36, 4, 44, 12, 52, 20, 60, 28,
	35, 3, 43, 11, 51, 19, 59, 27,
	34, 2, 42, 10, 50, 18, 58, 26,
	33, 1, 41, 9, 49, 17, 57, 25,
	32, 0, 40, 8, 48, 16, 56, 24,
)

EXPANSION = (
	31, 0, 1, 2, 3, 4,
	3, 4, 5, 6, 7, 8,
	7, 8, 9, 10, 11, 12,
	11, 12, 13, 14, 15, 16,
	15, 16, 17, 18, 19, 20,
	19, 20, 21, 22, 23, 24,
	23, 24, 25, 26, 27, 28,
	27, 28, 29, 30, 31, 0,
)

PERMUTATION = (
	15, 6, 19, 20, 28, 11, 27, 16,
	0, 14, 22, 25, 4, 17, 30, 9,
	1, 7, 23, 13, 31, 26, 2, 8,
	18, 12, 29, 5, 21, 10, 3, 24,
)

PERMUTED_CHOICE1 = (
	56, 48, 40, 32, 24, 16, 8,
	0, 57, 49, 41, 33, 25, 17,
	9, 1, 58, 50, 42, 34, 26,
	18, 10, 2, 59, 51, 43, 35,
	62, 54, 46, 38, 30, 22, 14,
	6, 61, 53, 45, 37, 29, 21,
	13, 5, 60, 52, 44, 36, 28,
	20, 12, 4, 27, 19, 11, 3,
)

PERMUTED_CHOICE2 = (
	13, 16, 10, 23, 0, 4,
	2, 27, 14, 5, 20, 9,
	22, 18, 11, 3, 25, 7,
	15, 6, 26, 19, 12, 1,
	40, 51, 30, 36, 46, 54,
	29, 39, 50, 44, 32, 47,
	43, 48, 38, 55, 33, 52,
	45, 41, 49, 35, 28, 31,
)

SUBSTITUTION_BOX = (
	(
		14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7,
		0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8,
		4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0,
		15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13,
	),
	(
		15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10,
		3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5,
		0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15,
		13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9,
	),
	(
		10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8,
		13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1,
		13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7,
		1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12,
	),
	(
		7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15,
		13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9,
		10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4,
		3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14,
	),
	(
		2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9,
		14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6,
		4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14,
		11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3,
	),
	(
		12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11,
		10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8,
		9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6,
		4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13,
	),
	(
		4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1,
		13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6,
		1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2,
		6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12,
	),
	(
		13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7,
		1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2,
		7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8,
		2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11,
	),
)

LEFT_SHIFTS = (
	1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1,
)


class DESBlock:
	def __init__(self, plainblock: bitarray):
		self.block = bitarray(plainblock)

	def initial_permutation(self):
		new_block = bitarray(64)
		for bit in range(len(new_block)):
			new_block[bit] = self.block[INITIAL_PERMUTATION[bit]]
		self.block = new_block

	def round(self, subkey: bitarray):
		left32 = self.block[:32]
		right32 = self.block[32:]

		# Expend
		expended = bitarray(48)
		for bit in range(len(expended)):
			expended[bit] = right32[EXPANSION[bit]]

		# XOR with subkey
		XORed = expended ^ subkey

		# Substitution (go through S-Box)
		substituted = bitarray(32)
		substituted_ptr = 0
		sboxes = iter(SUBSTITUTION_BOX)
		for i in range(0, len(XORed), 6):
			sixbits = XORed[i:i + 6]  # Split 48 bits into 8 groups, each as the input of the corresponding S-Box
			sbox = next(sboxes)  # Select the S-Box
			row_ind = (sixbits[0] << 1) + sixbits[5]  # Select row using the first and last bit
			col_ind = ba2int(sixbits[1:5])  # Select column using the middle 4 bits
			substituted[substituted_ptr:substituted_ptr + 4] = int2ba(sbox[row_ind * 16 + col_ind], length=4)
			substituted_ptr += 4

		# Permutation
		permuted = bitarray(32)
		for bit in range(len(permuted)):
			permuted[bit] = substituted[PERMUTATION[bit]]

		self.block = right32 + (permuted ^ left32)

	def preoutput(self):
		self.block = self.block[32:] + self.block[:32]

	def inverse_initial_permutation(self):
		new_block = bitarray(64)
		for bit in range(len(new_block)):
			new_block[bit] = self.block[INVERSE_INITIAL_PERMUTATION[bit]]
		self.block = new_block

	def tobytes(self):
		return self.block.tobytes()


def get_subkeys(key: bytes) -> List[bitarray]:
	"""
	Returns a list of 16 subkeys.
	Args:
	    key: 64 bits key, but only 56 bits are actually useful.
	"""
	# Permuted choice 1
	key_arr = bitarray()  # Little endian
	key_arr.frombytes(key)
	permuted1 = bitarray(56)
	for bit in range(len(permuted1)):
		permuted1[bit] = key_arr[PERMUTED_CHOICE1[bit]]

	left28 = permuted1[:28]
	right28 = permuted1[28:]

	subkeys = []
	for shift in LEFT_SHIFTS:
		# Ring left shift
		left28 = (left28 << shift) | (bitarray('0' * (28 - shift)) + left28[:shift])
		right28 = (right28 << shift) | (bitarray('0' * (28 - shift)) + right28[:shift])
		shifted = left28 + right28

		# Permuted choice 2
		permuted2 = bitarray(48)
		for bit in range(len(permuted2)):
			permuted2[bit] = shifted[PERMUTED_CHOICE2[bit]]
		subkeys.append(permuted2)

	return subkeys


def _single_block_DES(plaintext: bytes, key: bytes, is_encrypt: bool):
	block = bitarray()  # Little endian
	block.frombytes(plaintext)
	block = DESBlock(block)

	# Core algorithm
	block.initial_permutation()
	subkeys = get_subkeys(key)
	if not is_encrypt:
		# If decrypt, reverse the use of subkeys
		subkeys = reversed(subkeys)
	for subkey in subkeys:
		block.round(subkey)
	block.preoutput()
	block.inverse_initial_permutation()

	return block.tobytes()


def des_ecb(data: bytes, key: bytes, is_encrypt: bool) -> bytes:
	if len(data) % 8 != 0:
		raise Exception("Plaintext bit length must be a multiple of 64.")
	if len(key) % 8 != 0:
		raise Exception("Key must be 64 bits long.")

	final_ans = b''
	for block_start in range(0, len(data), 8):
		# Encrypt/Decrypt block by block
		final_ans += _single_block_DES(data[block_start:block_start + 8], key, is_encrypt)

	return final_ans


def des_cbc(data: bytes, iv: bytes, key: bytes, is_encrypt: bool):
	if len(data) % 8 != 0:
		raise Exception("Plaintext bit length must be a multiple of 64.")
	if len(key) % 8 != 0:
		raise Exception("Key must be 64 bits long.")
	if len(iv) % 8 != 0:
		raise Exception("IV must be 64 bits long.")

	if is_encrypt:
		final_ans = b''
		for block_start in range(0, len(data), 8):
			# IV^block before putting it into encryption 
			XORed = xor_bytes(iv, data[block_start:block_start + 8])
			result = _single_block_DES(XORed, key, is_encrypt)
			iv = result
			final_ans += result
	else:
		final_ans = b''
		prev_block = data[:8]
		for block_start in range(0, len(data), 8):
			result = _single_block_DES(data[block_start:block_start + 8], key, is_encrypt)
			if block_start == 0:
				result = xor_bytes(iv, result)
			else:
				result = xor_bytes(prev_block, result)
			final_ans += result
			prev_block = data[block_start:block_start + 8]

	return final_ans

# key = b'chopperc'
# iv = b'66666666'
# cipher = des_ecb(b'wowowowoeeeeeeee', key, True)
# print(cipher)
# deciphered = des_ecb(cipher, key, False)
# print(deciphered)
#
# cipher = des_cbc(b'wowowowoeeeeeeee', iv, key, True)
# print(cipher)
# deciphered = des_cbc(cipher, iv, key, False)
# print(deciphered)
