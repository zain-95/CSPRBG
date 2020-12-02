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

########################## Five basic statistical tests ##########################

All need a chi square distribution - I made it using gamma functions
(https://en.wikipedia.org/wiki/Gamma_function).

    * Frequency test (monobit test)

    A statistic to test if the number of 0's & 1's in a sequence s are approximately
    the same as the number of counts for a random sequence. For random sequence statistic
    should be chi square distribute with 1 degree of free dom (if n >= 10).

    * Serial test (two-bit test)

    A statistic on two-bit counts to test if the number of 00, 01, 10, 11 in a sequence s
    are approximately the same as the nombor of counts for a random sequence. For a random
    sequence statistic should be chi square distributed with 2 degrees of freedom
    (if n >= 21).

    * Poker test

    A statistic to test if the counts of non-overlapping m-bit parts in a sequence s is
    approximately the same as the number of counts for a random sequence. For a random
    sequence statistic should be chi square distributed with 2**m -1 degrees of freedom
    (with the number of non-overlaping m-bit parts, k = n // m, bigger than 5 * 2**m).

    A generalisation of the frequency test.

    * Runs test

    A statistic on the runs (both blocks & gaps) in a sequence s to test if the counts
    are approximately the same the number of counts for a random sequence. For a random
    sequence statistic should be chi square distributed with 2k-2 degrees of freedom.

    * Autocorrelation test

    A statistic on correlation of the binary sequence s with (non-cyclic) shifted (by d)
    version of itself. For a random sequence statistic should be a standard normal
    distribution if (n-d) >= 10. As small value of A(d) are as unexpected as big a
    two-sided test should be used.

########################## Python Requirements:##########################

    * sympy
    * Python 3
