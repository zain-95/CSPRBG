Cryptograpically Secure Pseudorandom Bit Generators

########################## Micali-Schnorr ##########################

    * "Improves the efficiency of the RSA PRBG"

    * My implementation takes 2 primes p & q, a starting seed x0 and the number of
      output bit.

    * y_(i+1) = x_i**e mod n

        - n = p * q
        - N is the number of bit in n
        - e is gcd(e,phi(n))=1, 80e <= N and 1<e<phi
        - k = floor(N * (1-2/e))
        - r = N - k
        - x_i is the r most significant bits of y_i
        - z_i are output as the k least signigicant bits of y_i
  
    For some primes some exponents have gcd(e, phi(n)) == 1 but do not satisfy
    80e <= N (why that condition?). My code gives a error message and returns False if
    it cannot find a e for a given p & q that meets the two conditions. Code works for
    primesize > 120.

    k = floor(N * (1-2/e)) seems big. Ive taken biggest possible e as the floor(N/80).
    The bigger e is the bigger the number of bit k taken per step.

    If the seed x0 is too small then my implementation uses sha256 hash repeatedly to make a
    r or bigger bit number (where r = N-k).
    
    "RSA-like primes" are recommended - I used Gordon's algorithm (for "Strong primes"). 
    It didn't noticeably improve the number of times a e can not be found.

########################## Python Requirements:##########################

    * sympy for gcd, nextprime
    * Python 3
