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
