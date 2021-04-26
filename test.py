from mycryptool.hash import md5, sha1
from mycryptool.symmetric import aes128
from mycryptool.asymmetric import elliptic_curve

print(md5.md5(b'basdfasdfadsf'))
print(sha1.sha1(b'basdfasdfadsf'))

data = b'Jessie Pinkman in the house'
key = 'key'
cypher = aes128.encrypt(key, data)
print(cypher)
print(aes128.decrypt(key, cypher))

ec = elliptic_curve.ecp256k1()
pri = ec.get_private_key()
pub = ec.get_public_key(pri)
ec_cypher = ec.encrypt(data, pub)
print(ec_cypher)
print(ec.decrypt(ec_cypher, pri))

sig = ec.get_signature(sha1.sha1(data), pri)
print(ec.is_valid_signature(sha1.sha1(data), sig, pub))
