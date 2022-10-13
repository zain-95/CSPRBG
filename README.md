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
    It didn't noticeably improve the number of times a e cannot be found.

########################## Blum-Blum-Shub ########################## 

    * Or the x**2 mod n generator.
    
    * My implementation takes 2 primes p & q, a starting seed s and the number of output bit
      numbit.
      
        - n = p * q
        - p & q is 3 mod 4
        - s is in interval [1, n-1]
        - s is gcd(s,n) == 1

    * x_(i+1) = x_i**2 mod n

        - x_0 = s**2 mod n
        - z_i output is the least significant bit of x_i for 1 <= i < numbits

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

    * FIPS 140-1

    Do 4 of the statistical tests on a random binary sequence of length = 20000 and check if
    the sequence passes all of them.

########################## Multivarate Quadratic DRBG ##########################

    * MQ_DRBG is based on iteration of a random multivarate quadratic system.

    * There are fixed lengths for the MQ_DRBG. My initial code handles the files.

    * Two functions suggested by the standard - field_vector() and flatten()

    * Works for all field sizes - and there is an error in field size 6 from the specification and the test vectors

    * Initialize state by hashing seed to get input vector of integers
      - Apply equations from parameter file to random state
        - Get two vectors of values from this
          - Vector y is the new state vector
          - Vector z is the output containing one block of bit to output
      - If not enough bits produced, run again with the state just returned
        - This will make another block of output

    * The seed needs to be as large as the block length. Pad with 0s if it is not

    * Generate 100 binary streams of 20000 bits and do the FIPS 140-1 tests on them

    * Test vectors

    I used the test vectors in the annex to the standard to check my code. The results did not match.
    This is because there are mistakes in the standard. I have changed my code to make the test vectors work.

    There is a problem with the endianness of the parameters and test vectors. If the state vector is like in the
    standard, the results produced are wrong. If it is reversed before it goes into the MQ_DRBG and the output of the
    MQ_DRBG is reversed then the results match the test vector.

    The parameter files are not formatted in the way they are suppose to be. The process in the standard says that the
    quadratic terms are listed with the non-linear terms, but to get the test vectors to match for field size 1 they
    have to be read with the linear terms. The code now reads the parameters in a way that works with the test vectors.

    The tests for field size 6 also did not work. This is because the irreducible polynomial for 6 in the standard is
    x**6+x+1, but for the test vectors to work, the polynomial is x**6+x**4+x**3+x+1. Code now uses polynomial that works
    with test vectors, not the one in the standard.

########################## Python Requirements:##########################

    * sympy
    * Python 3
