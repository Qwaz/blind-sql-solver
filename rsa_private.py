#!/usr/bin/env python3
import os
import subprocess
from subprocess import PIPE, STDOUT

p = int(input('p: '))
q = int(input('q: '))
e = input('e(default 0x10001): ')

if e: e = int(e)
else: e = 0x10001

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m

n = p*q
d = modinv(e, (p-1)*(q-1))
coeff = modinv(q, p)

in_file = '''asn1=SEQUENCE:private_key

[private_key]
version=INTEGER:0
modulus=INTEGER:{n}
pubExp=INTEGER:{e}
privExp=INTEGER:{d}
p=INTEGER:{p}
q=INTEGER:{q}
e1=INTEGER:{e1}
e2=INTEGER:{e2}
coeff=INTEGER:{coeff}
'''.format(n=n, e=e, d=d, p=p, q=q, e1=d % (p-1), e2=d % (q-1), coeff=coeff)

f = open('asn1.config', 'w')
f.write(in_file)
f.close()

p = subprocess.Popen(['openssl', 'asn1parse', '-genconf', 'asn1.config', '-out', 'private.der'], stdout=PIPE, stderr=STDOUT)
print(p.communicate()[0].decode('ascii'))

p = subprocess.Popen(['openssl', 'rsa', '-in', 'private.der', '-inform', 'der', '-text', '-check'], stdout=PIPE, stderr=STDOUT)
print(p.communicate()[0].decode('ascii'))

os.system('rm asn1.config private.der')
