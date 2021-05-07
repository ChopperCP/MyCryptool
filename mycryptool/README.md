# MyCrptool

___

A python package that include commonly used cryptographic algorithm and tools.

This package is designed as a teaching tool, written in pure python. It means that it probably won't be as efficient as
other similar python libraries which use C for low-level implementation and provide the same if not more functions.
However, the author try to write clean and simple code to demonstrate how a cryptography algorithm works.

GitHub repository (and newest documentation) : https://github.com/ChopperCP/MyCryptool

# Install

___

    pip install mycrptool

### Problem with bitarray

This package use `bitarray` as an external library. When installing this library, you may fail to compile.

If that's the case, you can go to https://www.lfd.uci.edu/~gohlke/pythonlibs/ to download a pre-compiled version
of `bitarray`, and then simply run:

    pip install downloaded-precompiled-file.whl

# Dependencies

___
Here are external libraries that is used in this package.

    bitarray

# Usage

___
This package consists of 4 parts: symmetric, asymetric, hash, and tools.

To import all modules, it is recommanded to run `from mycryptool import *`

## symmetric

***
This module includes 2 symmetric algorithms: AES128 and DES.

### AES128

The Default scheme is CBC. if you want to try other schemes, welcome to explore the AES class (in `symmetric.aes128`).

#### Encrypt:

    data = b'Jessie Pinkman in the house'
    key = 'key'
    cipher = symmetric.aes128.encrypt(key, data)

#### Decrypt:

    symmetric.aes128.decrypt(key, cipher)

### DES

DES only supports 2 schemes: CBC and ECB. Supported Features: encrypt and decrypt.

#### Encrypt:

```python
key = b'chopperc'
iv = b'66666666'
data = b'Yo Yo Yo, Jessie Pinkman in the house!!!'

cipher = symmetric.des.des_cbc(data, iv, key, True)  # CBC

cipher = symmetric.des.des_ecb(data, key, True)  # ECB
```

#### Decrypt:

```python
deciphered = symmetric.des.des_cbc(cipher, iv, key, False)  # CBC
deciphered = symmetric.des.des_ecb(cipher, key, False)  # ECB
```

## asymmetric

***
This module includes 2 asymmetric algorithms: RSA and Elliptic Curve.

Supported Features: encrypt, decrypt, generate signature, and validate signature.

### RSA

#### Encrypt:

```python
data = b'Jessie Pinkman in the house'
# Warning: it takes a while to generate key pairs ( large prime numbers).
pub, pri = asymmetric.rsa.generate_key_pair()
cipher = asymmetric.rsa.encrypt(data, pub)
```

#### Decrypt:

```python    
asymmetric.rsa.decrypt(cipher, pri)
```

#### Generate signature:

```python
signature = asymmetric.rsa.get_signature(hash.md5.md5(data), pri)
print(signature)
```

#### Validate signature:

```python
asymmetric.rsa.is_valid_signature(hash.md5.md5(data), signature, pub)
```

### Elliptic Curve

As for now, this module only supports 1 curve: ecp256k1.

However, you can Implement your own curve derived from the `EllipticCurve` class.

#### Implement customize curve:

```python
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
```

#### Encrypt:

```python
ec = asymmetric.elliptic_curve.ecp256k1()
pri = ec.get_private_key()
pub = ec.get_public_key(pri)
ec_cipher = ec.encrypt(data, pub)
print(ec_cipher)
```

#### Decrypt:

```python
ec.decrypt(ec_cipher, pri)
```

#### Generate signature:

```python
signature = ec.get_signature(hash.sha1.sha1(data), pri)
```

#### Validate signature:

```python
ec.is_valid_signature(hash.sha1.sha1(data), signature, pub)
```

## hash

___

### md5

This module provide 2 hashing algorithm: MD5 and SHA-1.

```python
    hash.md5.md5(b'basdfasdfadsf')
```

### sha1

```python
    hash.sha1.sha1(b'basdfasdfadsf')
```