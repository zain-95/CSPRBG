#!/usr/bin/env python3

from prbgfunctions import *
from tests import *

# tests of the BBS_PRBG

seed = 1077
primesize = 1024
ntrials = 100
alphasig = 0.01
automaxscore = 2.3263 # normal significance level of alphasig

failedfips = []
failedserial = []

random.seed(seed)

print("\nMaking {} random streams of 20000 bits using BBS_PRBG and testing with FIPS and serial...".format(ntrials))
print("Using primes of {} bits...".format(primesize))
for i in range(ntrials):
    p,q = randprime(primesize), randprime(primesize)
    while p%4 != 3:
        p = randprime(primesize)
    while q%4 != 3:
        q = randprime(primesize)
    n = p * q
    s = random.randint(1, n-1)
    bstream = bbs_prbg(p, q, s, 20000)
    if not passfips(bstream):
        failedfips.append((p, q, s))
        print("  {}. Found a case that failed FIPS.".format(i))
    stscore = serialtest(bstream)
    if chiprob(2, stscore) < alphasig:
        failedserial.append((p, q, s))
        print("  Found a PRBG with serial test score = {0:6.4} which is chi square prob = {1:7.3}".format(stscore, chiprob(2, stscore)))
         
print("\nOf the {} PRBGs made found {} that failed the FIPS test.".format(ntrials, len(failedfips)))
print("Of the {} PRBGs made found {} that failed the serial test at {} significance level. "
      "Expected to find {}.".format(ntrials, len(failedserial), alphasig, alphasig * ntrials))

print("\nTesting the autocorrelation shifts of a 20000 long PRBG from BBS_PRBG...")
p,q = randprime(primesize), randprime(primesize)
while p%4 != 3:
    p = randprime(primesize)
while q%4 != 3:
    q = randprime(primesize)
s = random.getrandbits(primesize)
bstream = bbs_prbg(p, q, s, 20000)
testauto = [ autocortest(bstream, i) for i in range(1, 20000//2 + 1) ]
maxauto, minauto = max(testauto), min(testauto)
if maxauto > automaxscore:
    print("Failed: Found autocorrelation score of {} at shift d = {} ".format(maxauto, testauto.index(maxauto) + 1))
if abs(minauto) > automaxscore:
    print("Failed: Found autocorrelation score of {} at shift d = {} ".format(minauto, testauto.index(minauto) + 1))
if maxauto < automaxscore and abs(minauto) < automaxscore:
    print("Passed: No shifts found with autocorrelation score bigger than {}".format(automaxscore))
