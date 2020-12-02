#!/usr/bin/env python3

from prbgfunctions import *
from tests import *

# tests of the Micali-Schnorr PRBG

seed = 1234
primesize = 256 # primesize needs to be at least 120 for this to work
ntrials = 100
alphasig = 0.01
automaxscore = 2.3263 # normal significance level of alphasig
usestrongprimes = False

failedprimes = []
failedserial = []
failedpoker = []

random.seed(seed)

print("\nMaking {} random streams of 10000 bit using MS_PRBG...".format(ntrials))
i = 0
while i < ntrials:
    if usestrongprimes:
        p,q = exactgordonprime(primesize), exactgordonprime(primesize)
    else:
        p,q = randprime(primesize), randprime(primesize)
    x_0 = random.getrandbits(primesize)
    bstream = ms_prbg(p, q, x_0, 10000)
    if not bstream:
        failedprimes.append((p, q))
        continue
    i += 1
    pscore = pokertest(bstream, 4)
    if chiprob(2**4 - 1, pscore) < alphasig:
        failedpoker.append((p, q, x_0))
        print("  Found a PRBG with poker test score = {0:6.4} which is chi square prob = {1:7.3}".format(pscore, chiprob(2**4 - 1, pscore)))
    stscore = serialtest(bstream)
    if chiprob(2, stscore) < alphasig:
        failedserial.append((p, q, x_0))
        print("  Found a PRBG with serial test score = {0:6.4} which is chi square prob = {1:7.3}".format(stscore, chiprob(2, stscore)))

print("\nTo get to {0} PRBG found {1} prime pairs (of size {2} bit) where a PRBG can't be made."
      "(Failure rate of {3:4.3}%)\n ".format(ntrials, len(failedprimes), primesize, 100.0 * len(failedprimes) / (ntrials + len(failedprimes))))
print("Of the {} PRBG made found {} that failed the poker test at {} significance level. "
      "Expected to find {}.".format(ntrials, len(failedpoker), alphasig, alphasig * ntrials))
print("Of the {} PRBG made found {} that failed the serial test at {} significance level. "
      "Expected to find {}.".format(ntrials, len(failedserial), alphasig, alphasig * ntrials))

print("\nTesting the autocorrelation shifts of a 20000 long PRBG from MS_PRBG...")
bstream = False
while not bstream:
    p, q = randprime(primesize), randprime(primesize)
    x_0 = random.getrandbits(primesize)
    bstream = ms_prbg(p, q, x_0, 20000)
testauto = [ autocortest(bstream, i) for i in range(1, 20000//2 + 1) ]
maxauto, minauto = max(testauto), min(testauto)
if maxauto > automaxscore:
    print("Failed: Found autocorrelation score of {} at shift d = {} ".format(maxauto, testauto.index(maxauto) + 1))
if abs(minauto) > automaxscore:
    print("Failed: Found autocorrelation score of {} at shift d = {} ".format(minauto, testauto.index(minauto) + 1))
if maxauto < automaxscore and abs(minauto) < automaxscore:
    print("Passed: No shifts found with autocorrelation score bigger than {}".format(automaxscore))
