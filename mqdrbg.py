#!/usr/bin/env python3

from paramtable import paramdict

requested_block_length = 256
requested_strength = 256

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
print("Done.")
