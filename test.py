from mycryptool.hash import md5, sha1
from mycryptool.symmetric import aes128
from mycryptool.asymmetric import elliptic_curve, rsa
from mycryptool.tools import *

print(md5.md5(b'basdfasdfadsf'))
print(sha1.sha1(b'basdfasdfadsf'))

data = b'Jessie Pinkman in the house'
key = 'key'
# cipher = aes128.encrypt(key, data)
# print(cipher)
# print(aes128.decrypt(key, cipher))
#
# ec = elliptic_curve.ecp256k1()
# pri = ec.get_private_key()
# pub = ec.get_public_key(pri)
# ec_cipher = ec.encrypt(data, pub)
# print(ec_cipher)
# print(ec.decrypt(ec_cipher, pri))
#
# sig = ec.get_signature(sha1.sha1(data), pri)
# print(ec.is_valid_signature(sha1.sha1(data), sig, pub))
#
# print(is_prime(65537))

# print(generate_prime(1024))

# pub, pri = rsa.generate_key_pair()
# cipher = rsa.encrypt(data, pub)
# print(cipher)
# print(rsa.decrypt(cipher, pri))
#
# sig = rsa.get_signature(md5.md5(data), pri)
# print(sig)
# print(rsa.is_valid_signature(md5.md5(data), sig, pub))
