from prbgfunctions import *

def field_vector(bit_array, field_size):
    """Given a list bit_array of bits (with length a multiple of field_size), returns an array of integers, where each
         integer is the value of next group of a field_size number of bits.
       That is, bvec[0] = 0b(bit_array[0]||bit_array[1]||...bit_array[field_size-1])
            and bvec[1] = 0b(bit_array[field_size]||bit_array[field_size+1]||...bit_array[2*field_size-1]) ..."""
    if field_size == 1: # in this case, integers are 0's and 1's, and same as original bit string
        return bit_array
    in_len = len(bit_array)
    if in_len%field_size != 0:
        print("ERROR: Length of the input is not a multiple of the field size")
        exit(1)
    bvec = []
    for i in range(in_len//field_size):
        bvec.append(bits_to_int(bit_array[i*field_size:(i+1)*field_size]))
    return bvec

def flatten(bvec, field_size):
    """Given a list of integers of field_size bits, returns an array of the concatenated bits of bvec[0]...bvec[-1].
       Returns original bitstring input into function field_vector(bit_array, field_size) when applied to its output."""
    if field_size == 1:
        return bvec
    bit_array = []
    for i in bvec:
        bit_array += int_to_bits(i, field_size)
    return bit_array

def bfmult(a,b, field_size):
    """Multiplication of a and b over binary field of size field_size."""
    if field_size == 1:
        return a * b
    elif field_size in [2,3,4]: # for field_size in [2,3,4], x**field_size becomes (x+1) = 0b11
        pmod = 0b11
    elif field_size == 6: # for field_size=6, x**6 reduces to x**4+x**3+x+1 = 0b011011
                          # (NOT x**6+x+1 as indicated by standard)
        pmod = 0b011011
    elif field_size == 8: # for field_size=8, x**8 reduces to x**4+x**3+x**2+1 = 0b11101
        pmod = 0b11101
    else:
        print("ERROR: Unsupported field size: {}".format(field_size))
        exit(1)

    fexp = 2**field_size
    prod = 0
    for i in range(field_size):
        prod ^= (((a>>i) & 1) * b) << i
    bfproduct = prod % fexp
    highbits = prod // fexp
    for i in range(field_size):
        bfproduct ^= ((highbits>>i) & 1) * (pmod<<i)
    while bfproduct >= fexp:
        highbits = bfproduct // fexp
        bfproduct = bfproduct % fexp
        for i in range(field_size):
            bfproduct ^= ((highbits>>i) & 1) * (pmod<<i)
    return bfproduct

def Evaluate_MQ(P, x, state_length = 272, block_length = 256, field_size = 1):
    """Given a state x as an array of bits and forward and output MQ equations in P, 
         returns the next internal state and the output state."""
    P_vec = field_vector(P, field_size) # coefficients for MQ equations (as integer vector)
    # input state x (as integer vector). Reversed since coefficient files expect least-significant bits *first*,
    #     while test vectors have least-significant *last*; so reverse here, then reverse output after computations
    x_vec = list(reversed(field_vector(x, field_size)))
    y_vec = field_vector([0] * state_length, field_size) # updated state (as integer vector)
    z_vec = field_vector([0] * block_length, field_size) # output block (as integer vector)
    n = state_length//field_size
    m = block_length//field_size
    t = 0
    for i in range(n): # compute new state using MQ equations
        for j in range(n): # nonlinear terms a_jk * x_j * x_k
            for k in range(j, n):
                if field_size==1 and j==k: # for field size=1, x_j*x_j=x_j. do with linear terms below.
                    continue
                y_vec[i] = y_vec[i] ^ bfmult(P_vec[t], bfmult(x_vec[j], x_vec[k], field_size), field_size)
                t += 1
        for j in range(n): # linear terms b_j * x_j
            y_vec[i] = y_vec[i] ^ bfmult(P_vec[t], x_vec[j], field_size)
            t += 1
        y_vec[i] = (y_vec[i] ^ P_vec[t]) # constant term c
        t += 1
    for i in range(m): # compute new block using MQ equations
        for j in range(n): # nonlinear terms a_jk * x_j * x_k
            for k in range(j, n):
                if field_size==1 and j==k: # for field size=1, x_j*x_j=x_j. do with linear terms below.
                    continue
                z_vec[i] = z_vec[i] ^ bfmult(P_vec[t], bfmult(x_vec[j],  x_vec[k], field_size), field_size)
                t += 1
        for j in range(n): # linear terms b_j * x_j
            z_vec[i] = z_vec[i] ^ bfmult(P_vec[t], x_vec[j], field_size)
            t += 1
        z_vec[i] = z_vec[i] ^ P_vec[t] # constant term c
        t += 1
    return flatten(list(reversed(y_vec)), field_size), flatten(list(reversed(z_vec)), field_size)

def MQ_DRBG(P, inx, numbits, state_length, block_length, field_size):
    """Given a starting seed inx and coefficients of MQ equations in P,
       returns numbits of bits from MQ_DRBG using the state_length, block_length, and field_size. """
    x = inx[:]
    if len(x) < state_length: # if seed not large enough, pad with zeros
        x = [0] * (state_length - len(x)) + x
    randbits_mq = []
    while len(randbits_mq) < numbits:
        y,z = Evaluate_MQ(P, x, state_length, block_length, field_size)
        randbits_mq += z
        x = y
    return randbits_mq[:numbits]
