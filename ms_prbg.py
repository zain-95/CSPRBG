import math, random, hashlib
from sympy import gcd, nextprime

def ms_prbg(p, q, x_0, numbits, usehash = True):
    """Micali-Schnorr PRBG:
       Primes p & q give modulus n = p * q. Sequence is y_(i+1) = x_i**e mod n.
       N: the number of bit in n
       e: gcd(e, phi(n))=1, 80e <= N, and 1<e<phi
       k = floor(N * (1-2/e)): number of bit of y_i to output
       r = N-k: number of most significant bit of y_i that give x_i for next iteration
       usehash makes starting seed a r bit or bigger number, if x0 too small,
           by repeated sha256 hashing"""
    n = p * q
    phi = (p-1) * (q-1)
    N = n.bit_length()
    # Try different values for expon until expon and phi have a gcd of 1
    expon = 3
    while gcd(expon, phi) != 1:
        expon = expon + 2
    if 80 * expon > N:  
        print("ERROR: Could not find a e with gcd(e, phi(n)) == 1 and 80e <= N")
        return False
    k = int(math.floor(N * (1 - 2.0/expon)))
    # Calculate 2**k once for efficient
    kexp = 2**k
    r = N - k
    randbits_ms = []  # array for the integers z_i that make the random output sequence
    x = x_0
    while x.bit_length() < r and usehash:
        x = (x << 256) | int('0x'+sha256hash(x), 16)
    l = numbits//k + 1
    for i in range(l):
        y = pow(x, expon, n)
        x = y >> k # k = N - r so get r most significant bit
        z = y & (kexp-1) # k least significant bits
        randbits_ms += int_to_bits(z, k)
    return randbits_ms[:numbits]

def randprime(k):
    """Returns a random prime of k bit """
    p = 0
    while p.bit_length() < k:
        p = nextprime(random.getrandbits(k))
    return p

def int_to_bits(x, k = -1):
    """Returns a array of 0,1's of the bits of a integer x.
       Use k to give total number of bit needed in case highest bit are 0 """
    bit_array = list(reversed([ int((x >> i) & 1) for i in range(x.bit_length()) ]))
    if len(bit_array) < k:
        return [0] * (k-len(bit_array)) + bit_array
    return bit_array

def inttobytes(num):
    """Given a int change it to bytes """
    return num.to_bytes((num.bit_length() + 7) // 8, 'big')

def sha256hash(num):
    """Returns the sha256 hash (as a hex string) of the given int """
    if type(num) == int:
        inbytes = inttobytes(num)
        return hashlib.sha256(inbytes).hexdigest()

# test run of the Micali-Schnorr PRBG

primesize = 256
p,q = randprime(primesize), randprime(primesize)
x_0 = random.getrandbits(primesize)
print(ms_prbg(p, q, x_0, 10))
