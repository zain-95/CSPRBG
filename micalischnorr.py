#!/usr/bin/env python3

from prbgfunctions import *

# test of the Micali-Schnorr PRBG

seed = 1234
primesize = 256 # primesize needs to be at least 120 for this to work
ntrials = 100
usestrongprimes = False

failedprimes = []

random.seed(seed)

print("\nMaking {} random streams of 1000 bit using MS_PRBG...".format(ntrials))
i = 0
while i < ntrials:
    if usestrongprimes:
        p,q = exactgordonprime(primesize), exactgordonprime(primesize)
    else:
        p,q = randprime(primesize), randprime(primesize)
    x_0 = random.getrandbits(primesize)
    bstream = ms_prbg(p, q, x_0, 1000)
    if not bstream:
        failedprimes.append((p, q))
        continue
    i += 1

print("\nTo get to {0} PRBG found {1} prime pairs (of size {2} bit) where a PRBG can't be made."
      "(Failure rate of {3:4.3}%)\n ".format(ntrials, len(failedprimes), primesize, 100.0 * len(failedprimes) / (ntrials + len(failedprimes))))
