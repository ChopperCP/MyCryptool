# from mycryptool.hash import md5, sha1
# from mycryptool.symmetric import aes128, des
# from mycryptool.asymmetric import elliptic_curve, rsa
# from mycryptool.tools import *
from mycryptool import *
from bitarray import bitarray

print(hash.md5.md5(b'basdfasdfadsf'))
print(hash.sha1.sha1(b'basdfasdfadsf'))
#
data = b'Jessie Pinkman in the house'
key = 'key'
# cipher = aes128.encrypt(key, data)
# print(cipher)
# print(aes128.decrypt(key, cipher))
#
# ec = asymmetric.elliptic_curve.ecp256k1()
# pri = ec.get_private_key()
# pub = ec.get_public_key(pri)
# ec_cipher = ec.encrypt(data, pub)
# print(ec_cipher)
# print(ec.decrypt(ec_cipher, pri))
#
# sig = ec.get_signature(hash.sha1.sha1(data), pri)
# print(ec.is_valid_signature(hash.sha1.sha1(data), sig, pub))
#
# print(is_prime(65537))

# print(generate_prime(1024))

# pub, pri = asymmetric.rsa.generate_key_pair()
# cipher = asymmetric.rsa.encrypt(data, pub)
# print(cipher)
# print(asymmetric.rsa.decrypt(cipher, pri))
#
# signature = asymmetric.rsa.get_signature(hash.md5.md5(data), pri)
# print(signature)
# print(asymmetric.rsa.is_valid_signature(hash.md5.md5(data), signature, pub))

# print(tools.xor_bytes(b'66666666', b'chopperc'))

# key = b'chopperc'
# iv = b'66666666'
# data = b'Yo Yo Yo, Jessie Pinkman in the house!!!'
# cipher = symmetric.des.des_ecb(data, key, True)
# print(cipher)
# deciphered = symmetric.des.des_cbc(cipher, iv, key, False)
# print(deciphered)

# data = b'Jessie Pinkman in the house'
# key = 'key'
# cipher = symmetric.aes128.encrypt(key, data)
# print(cipher)
# print(symmetric.aes128.decrypt(key, cipher))
