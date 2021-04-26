import random
from mycryptool.tools import *


class EllipticCurve:
	def __init__(self, a, b, p, G, n):
		# Elliptic curve equation: y^2 mod p = (x^3+ax+b) mod p.
		self.a = a
		self.b = b
		self.p = p
		self.G = G  # Generator, 2-element tuple.
		self.n = n  # rank of the generator.

	def is_on_curve(self, point):
		# Determine whether a point is on the curve.
		x, y = point
		lhs = (y * y) % self.p
		rhs = (x ** 3 + self.a * x + self.b) % self.p
		if lhs == rhs:
			return True
		return False

	def invert(self, point):
		# Calculate the (add operation) invert of a point.
		return (point[0], -point[1] % self.p)

	def add(self, p1, p2):
		"""
		Returns the sum of 2 points.
		p1 and p2 are points (2-element tuple).
		NOTICE: O=(0,0) is the infinitely far point, also the identity element ( of addition).
		"""

		if p1 is None:
			# 0 + p2 == p2
			return p2
		if p2 is None:
			# p1 + 0 == p1
			return p1

		# Result not on curve.
		if self.is_on_curve(p1) == False or self.is_on_curve(p2) == False:
			return (0, 0)

		# p+(-p)==(0,0)
		if (p1[0] == p2[0] and p1[1] == -p2[1]):
			return (0, 0)

		l = 0  # lambda in the formula.
		if tuple(p1) == tuple(p2):
			l = ((3 * p1[0] * p1[0] + self.a) * invert(2 * p1[1], self.p)) % self.p
		else:
			numerator = p2[1] - p1[1]
			denominator = p2[0] - p1[0]
			l = (numerator * invert(denominator, self.p)) % self.p

		x = ((l * l) - p1[0] - p2[0]) % self.p
		y = (l * (p1[0] - x) - p1[1]) % self.p

		return (x, y)

	def multiply(self, k, point):
		# Scalar multiply.
		assert self.is_on_curve(point)

		if k < 0:
			# k * point == -k * (-point)
			return self.multiply(-k, self.invert(point))

		result = None
		temp = point

		while k:
			if k & 1:
				# Add.
				result = self.add(result, temp)

			# Double.
			temp = self.add(temp, temp)

			k >>= 1

		assert self.is_on_curve(result)
		return result

	def get_private_key(self):
		# Randomly generate private key.
		return random.randint(1, self.n)

	def get_public_key(self, private_key: int):
		if (private_key <= self.n):
			return self.multiply(private_key, self.G)

	def encrypt(self, plain: bytes, pub):
		# ElGamal
		def insert_plain(plain):
			# Insert the plain onto the curve, returns a point.
			k = 32  # Left shift 5 binary digits.
			for i in range(0, k):
				x = bytes2int(plain) << 5 + i
				# Solve y in y^2==x^3+a*x+b
				rhs = (x ** 3 + self.a * x + self.b) % self.p
				# if p is an odd prime, p is quadratic residue<=>(x^3+a*x+b)^((p-1)/2)==1 mod p.
				if pow(rhs, (self.p - 1) >> 1, self.p) == 1:
					if (self.p % 4 == 3):
						# p==4n+3
						y = pow(rhs, (self.p + 1) >> 2, self.p)
						return (x, y)
					else:
						return (x, get_iroot(x, self.p)[0])  # y could be any one of the iroots.

		Pm = insert_plain(plain)  # Point after insertion.
		r = random.randint(1, self.n)
		# Cipher text == (k*G,Pm+k*pub)
		return self.multiply(r, self.G), self.add(Pm, self.multiply(r, pub))

	def decrypt(self, cipher, pri):
		# ElGamal
		def uninsert_plain(Pm):
			# Extract plain from a point.
			x, y = Pm
			k = 32  # Right shift 5 binary digits.
			plain = x >> 6  # Should be 6, don't know why, but it works!
			return int2bytes(plain)

		# Cipher text == (k*G,Pm+k*pub)
		# Pm=Pm+k*pub-pri*k*G=Pm+k*pri*G-pri*k*G
		Pm = self.add(cipher[1],
		              self.invert(self.multiply(pri, cipher[0])))  # Point after insertion.
		return uninsert_plain(Pm)

	def get_signature(self, plain_hash: bytes, pri):
		# ECDSA
		r = random.randint(1, self.n)
		s = (r - bytes2int(plain_hash) * pri) % self.n
		if s == 0:
			# Recalculate
			return self.get_signature(plain_hash, pri)
		return (r, s)

	def is_valid_signature(self, plain_hash: bytes, signature, pub):
		# ECDSA
		r, s = signature
		# s*G+hash*pri*G == (r-hash*pri)*G+hash*pri*G == r*G
		if self.add(self.multiply(s, self.G), self.multiply(bytes2int(plain_hash), pub)) == self.multiply(r, self.G):
			return True
		return False


class ecp256k1(EllipticCurve):
	# ecp256k1 https://www.secg.org/sec2-v2.pdf
	def __init__(self):
		a = 0
		b = 7
		p = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
		Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
		Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
		n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

		super(ecp256k1, self).__init__(a, b, p, (Gx, Gy), n)
