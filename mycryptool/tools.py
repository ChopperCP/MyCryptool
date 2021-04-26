import math
import functools


@functools.lru_cache()
def invert(k: int, mod: int):
	# Returns the invert of k

	if k == 0:
		raise ZeroDivisionError('division by zero')

	if k < 0:
		# k ** -1 = p - (-k) ** -1 (mod p)
		return mod - invert(-k, mod)

	# Extended Euclidean algorithm.
	s, old_s = 0, 1
	t, old_t = 1, 0
	r, old_r = mod, k

	while r != 0:
		quotient = old_r // r
		old_r, r = r, old_r - quotient * r
		old_s, s = s, old_s - quotient * s
		old_t, t = t, old_t - quotient * t

	gcd, x, y = old_r, old_s, old_t

	assert gcd == 1
	assert (k * x) % mod == 1

	return x % mod


def quick_power(base: 'int >=0', power: 'int >=0', mod: 'int >=0'):
	"""
	Returns base^power%mod.

	Args:
		base: base number, integer, >=0.
		power: nth power, integer, >=0.
		mod: modular, integer, >=0.
	"""
	base = base % mod
	ans = 1
	while power != 0:
		if power & 1:
			ans = (ans * base) % mod
		power >>= 1
		base = (base * base) % mod
	return ans


def is_have_iroot(x: 'int > 0', p: int):
	"""
		Returns whether x has an integer square root, that is
		whether there exist a y where y*y=x mod p，
		NOTICE: This function use a formula to determine and does not actually calculate the result,
		therefore, it is very efficient.
		It is suggested to check whether a iroot exists before actually calculating it.

		Args:
			x: integer, >=0 and <p.
			p: prime number
	"""
	ret = quick_power(x, (p - 1) // 2, p)
	if ret == 1:
		return True
	else:
		return False


def get_iroot(x: 'int >0 and int < p', p):
	"""
		Returns y (integer square root of x), where
		y*y=x mod p，已知x，p求y

		Args:
			x: integer, >=0 and <p.
			p: prime number
	"""
	t = 0
	# p-1=(2^t)*s //s is a odd number
	s = p - 1
	while s % 2 == 0:
		s = s // 2
		t = t + 1
	if t == 1:
		ret = quick_power(x, (s + 1) // 2, p)
		return ret, p - ret
	elif t >= 2:
		x_ = quick_power(x, p - 2, p)
		n = 1
		while is_have_iroot(n, p):
			n = n + 1
		b = quick_power(n, s, p)
		ret = quick_power(x, (s + 1) // 2, p)
		t_ = 0
		while t - 1 > 0:
			if quick_power(x_ * ret * ret, 2 ** (t - 2), p) == 1:
				pass
			else:
				ret = ret * (b ** (2 ** t_)) % p
			t = t - 1
			t_ = t_ + 1
		return ret, p - ret
	else:
		raise Exception()


def bytes2int(bytes):
	result = 0

	for b in bytes:
		result = result * 256 + int(b)

	return result


def int2bytes(value: int):
	length = math.ceil(value.bit_length() / 8)
	result = []

	for i in range(0, length):
		result.append(value >> (i * 8) & 0xff)

	result.reverse()

	return bytes(result)


def is_prime(n, k=5):
	"""
	Implementation uses the Miller-Rabin Primality Test
	The optimal number of rounds for this test is 40
	See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
	for justification

	Args:
		n: integer, number to be checked
		k: security parameter, false positive rate is 2^-k
	"""

	import random

	if n == 2:
		return True

	if n % 2 == 0:
		return False

	r, s = 0, n - 1
	while s % 2 == 0:
		r += 1
		s //= 2
	for _ in range(k):
		a = random.randrange(2, n - 1)
		x = pow(a, s, n)
		if x == 1 or x == n - 1:
			continue
		for _ in range(r - 1):
			x = pow(x, 2, n)
			if x == n - 1:
				break
		else:
			return False
	return True


def generate_prime(bit_length: 'int >=2'):
	if bit_length >= 1024:
		print("[!] Generating big prime, it may take a while...")
	import random

	p = random.randint(2 ** (bit_length - 1) + 1, 2 ** bit_length) | 1  # generate only odd numbers
	while not is_prime(p):
		p += 2
	return p
