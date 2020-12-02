import math
from sympy import lowergamma, gamma

from prbgfunctions import *

def chiprob(v, x):
    """Return the probability a random variable X with chi square distribution of v degree of freedom is bigger
       than value x ."""
    return 1 - float(lowergamma(v/2, x/2) / gamma(v/2))

def freqtest(s):
    """Returns a statistic on if the number of 0's & 1's in a sequence (represented as a array) is as expected
       for a random sequence.
       For a random sequence statistic should be chi square distributed with 1 degree of freedom (if n >= 10) """
    X_1 = (s.count(0) - s.count(1))**2 / len(s)
    return X_1

def serialtest(s):
    """Returns a statistic on if the two-bit counts of 00, 01, 10, 11 in a binary sequence (represented as a array of
       0's & 1's) is as expected for a random sequence.
       For a random sequence statistic should be chi square distributed with 2 degrees of freedom (if n >= 21) """
    n = len(s)
    ncount = [0] * 4
    for i in range(n-1):
        dbit = s[i:i+2]
        if dbit == [0,0]:
            ncount[0] += 1
        if dbit == [0,1]:
            ncount[1] += 1
        if dbit == [1,0]:
            ncount[2] += 1
        if dbit == [1,1]:
            ncount[3] += 1
    dibit_sum = sum([i**2 for i in ncount])
    monobit_sum = (s.count(0)**2 + s.count(1)**2)
    X_2 = (4.0/(n-1) * dibit_sum) - (2.0/n * monobit_sum) + 1
    return X_2

def pokertest(s, m):
    """Returns a statistic on m-bit counts in a binary sequence.
       For a random sequence statistic should be chi square distributed with 2**m -1 degrees of freedom.
       Needs the number of non-overlapping m-bit segments k = len(s)//m to be bigger than 5 * 2**m.   """
    n = len(s)
    k = int(math.floor(n/m)) # nombor of parts to break s into
    mexp = 2**m
    if k < 5 * mexp: # need at least 5 * 2**m parts
        return False
    ncount = [0] * mexp
    # Count occurrences of each bitstring of length m
    for j in range(k):
        val = bits_to_int(s[j*m:(j+1) * m])
        ncount[val] += 1
    seq_sum = sum([i**2 for i in ncount])
    X_3 = mexp/k * seq_sum - k
    return X_3

def blocksandgaps(s):
    """Given a binary sequence s returns dicts with counts for all seen sizes of blocks & gaps """
    teststr = "".join([str(i) for i in s ])
    B, G = {}, {} # dicts for counts of blocks & gaps
    blist = [i for i in teststr.split('0') if i ]
    glist = [i for i in teststr.split('1') if i ]
    bmax = len(max(blist)) # size of longest block
    gmax = len(max(glist)) # size of longest gap
    for i in range(1,max([gmax, bmax]) + 1): # count for both up to biggest gap or block
        B[i] = blist.count('1' * i)
        G[i] = glist.count('0' * i)
    return B, G

def runstest(s):
    """Given a sequence s returns a statistic on the runs (both blocks & gaps) in the sequence.
       Computes statistic over all lengths up to k.
       k: the run length where the size for len(s) is >=5.
       Returns the degrees of freedom 2k-2 and the statistic that follows a chi square distribution with that
       degrees of freedom."""
    B, G = blocksandgaps(s)
    n = len(s)
    i, X_4 = 1, 0
    elist = [ (n-i+3)/2**(i+2) ]
    while elist[i-1] >= 5: # for every gap (or block) size i where at least 5 are expected for sequence of length n
        i += 1
        elist.append((n-i+3)/2**(i+2))
    elist = elist[:-1]
    k = len(elist)
    for i in range(1, k+1):
        X_4 += ((B.get(i, 0) - elist[i-1])**2 + (G.get(i, 0) - elist[i-1])**2) / elist[i-1]
    return 2*k-2, X_4

def autocortest(s, d):
    """Returns a statistic on correlations of the binary sequence s with (non-cyclic) shifted (by d) versions of itself.
       For a random sequence statistic should be a standard normal distribution if (n-d) >= 10.
       As small values of A(d) are as unexpected as big, a two-sided test should be used. """
    n = len(s)
    maxd = min(n-10, n//2)
    if d > maxd:
        return False
    A = sum([ s[i] ^ s[i+d] for i in range(n-d) ])
    X_5 = 2 * (A - (n-d)/2) / math.sqrt(n-d)
    return X_5
