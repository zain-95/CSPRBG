#!/usr/bin/env python3

from mqdrbgfunctions import *
from paramtable import paramdict
from tests import *

requested_block_length = 256
requested_strength = 256
seed = 1
rand_file = None
ntrials = 100
alphasig = 0.01
automaxscore = 2.3263 # normal significance lvl of alphasig

failedfips = []
failedserial = []
bstreamlist = []

try:
    param_file, strength, state_length, block_length, field_size = paramdict["{}_{}".format(requested_block_length, requested_strength)]
except:
    print("ERROR: Could not find parameters for the requested strength {} and block length {}".format(requested_strength, requested_block_length))
    exit(1)
try:
    paramfile = open("params/" + param_file, "rb")
    data = paramfile.read()
    paramfile.close()
except:
    print("ERROR: Could not open file with multivariate quadriatic equations: {}".format(param_file))
    exit(1)
P = list()
for b in data:
    P += int_to_bits(b, 8)

print("\nMaking {} random streams of 20000 bits using MQ_DRBG and testing each with FIPS and serial...".format(ntrials))
i = 0
while i < ntrials:
    x = int_to_bits(seed + i, state_length) # set initial state of MQ_DRBG
    bstream = MQ_DRBG(P, x, 20000, state_length, block_length, field_size)
    if not bstream:
        continue
    else:
        bstreamlist.append(bstream)
        print("   Created random stream #{}.".format(i))
    i +=1
    if not passfips(bstream):
        failedfips.append(seed+i)
        print("  Found a case that failed FIPS.")
    stscore = serialtest(bstream)
    if chiprob(2, stscore) < alphasig:
        failedserial.append(seed+i)
        print("  Found a DRBG with serial test score = {0:6.4} which is chi square prob = {1:7.3}".format(stscore, chiprob(2,stscore)))

print("Of the {} DRBGs generated, found {} that failed the FIPS random test.".format(ntrials, len(failedfips)))
print("Of the {} DRBGs generated, found {} that failed the serial test at {} significance level. "
      "Expected to find {}.".format(ntrials, len(failedserial), alphasig, alphasig * ntrials))

print("\nTesting the autocorrelation shifts of a 20000 long DRBG from MQ_DRBG...")
bstream = bstreamlist[0]
testauto = [ autocortest(bstream, i) for i in range(1,20000-10)]
maxauto, minauto = max(testauto), min(testauto)
if maxauto > automaxscore:
    print("Failed: Found autocorrelation score of {} at shift d = {} ".format(maxauto, testauto.index(maxauto)+ 1))
if abs(minauto) > automaxscore:
    print("Failed: Found autocorrelation score of {} at shift d = {} ".format(minauto, testauto.index(minauto)+ 1))
if maxauto < automaxscore and abs(minauto) < automaxscore:
    print("Passed: No shifts found with autocorrelation score greater than {}".format(automaxscore))
print("\n")
