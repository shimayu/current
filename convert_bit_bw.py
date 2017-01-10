import sys
import numpy as np
from PIL import Image

Byte_size = 8

# the number of handlers
Addr_size = 256
Wide_size = 16
Raw_size = 16


def create_bw(data_arr):
    bitmap = []
    for i in xrange(Raw_size):
        for bit in xrange(Byte_size*2):
            if (data_arr[i] >> bit) & 1 == 1:
                # black(0)
                color = 0
            else:
                # white(255)
                color = 255
            bitmap.append([color, color, color])
    return bitmap

def create_white():
    bitmap = []
    color = 255
    for i in xrange(Raw_size):
        for bit in xrange(Byte_size*2):
            bitmap.append([color, color, color])
    return bitmap


if __name__ == '__main__':
    argvs = sys.argv

    f = open(argvs[1], "rb")
    data = f.read()
    byte = []
    for i in xrange(len(data)):
        byte.append(ord(data[i]))

    bw_arr = []
    byte_arr = []

    for x in byte:
        if len(byte_arr) < Raw_size:
            byte_arr.append(x)
        else:
            bw_arr.append(create_bw(byte_arr))
            bw_arr.append(create_white())
            byte_arr = [x]
            
    ip = Image.fromarray(np.uint8(np.array(bw_arr)))
    ip.save(argvs[2])

