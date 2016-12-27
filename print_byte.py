# Usage #
# python print_byte.py <b_file> 

import sys
import numpy as np
from PIL import Image

N_byte = 4

# the number of handlers
Addr_size = 256
Wide_size = 16
Raw_size = 16


def identify_func(byte):
    argn = []
    
    print("Input <byte_1> <byte_2> <byte_3> <byte_4>: ")
    for i in xrange(N_byte):
        print("Input <byte_{0}>: ".format(i+1))
        argn.append(int(raw_input('>>> '), 16))

    for i in range(3, len(byte)):
        if byte[i] == argn[3]:
            if byte[i-1] == argn[2]:
                if byte[i-2] == argn[1]:
                    if byte[i-3] == argn[0]:
                        print("Matching: 0x{0} = {1}"
                              .format(hex(argn[0]), i-3))


if __name__ == '__main__':
    argvs = sys.argv

    f = open(argvs[1], "rb")
    data = f.read()
    byte = []
    
    for i in xrange(len(data)):
        byte.append(ord(data[i]))

    while str != 'no':
        identify_func(byte)
        str = raw_input('continue? [yes/no]: ')
        
        
    
