#!/usr/bin/env python3

from mqdrbgfunctions import *
from paramtable import paramdict

requested_block_length = 256
requested_strength = 256
seed = 1
rand_file = None
ntrials = 100

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

print("\nMaking {} random streams of 1000 bits using MQ_DRBG...".format(ntrials))
i = 0
while i < ntrials:
    x = int_to_bits(seed + i, state_length) # set initial state of MQ_DRBG
    bstream = MQ_DRBG(P, x, 1000, state_length, block_length, field_size)
    if not bstream:
        continue
    else:
        print("   Created random stream #{}.".format(i))
    i +=1
