# Usage #
# python auto_connecting_normal.py <.csv file> <file_start_point>

import numpy as np
import struct
import sys

ELF_SIZE = 16
FILE_NUM = 25
FILE_BYTE = 1440
BYTE_SIZE = 960
THRESHOLD = 700
HEADER1_LOCATE = 112

def main():
    print("Cannot create any more files. Exit...")
    return 0

def cutting_func(byte, start, end):
    cutting = []

    # print("start_byte_locate: byte[{0}] = 0x{1}"
    #       .format(start, hex(byte[start])))
    # print("end_byte_locate: byte[{0}] = 0x{1}"
    #       .format(end, hex(byte[end])))
    for i in range(start, end + 1):
        cutting.append(byte[i])
    print("size: {0} byte".format(len(cutting)))
    return cutting

def cutting_header1_func(byte):
    cutting_header1 = []

    for i in xrange(HEADER1_LOCATE):
        cutting_header1.append(byte[i])
    return cutting_header1

# def cutting_header2_func(byte):
#     cutting_header2 = []

#     for i in range(360, len(byte)):
#         cutting_header2.append(byte[i])

#     return cutting_header2

def insert_zero(index):
    num = index % ELF_SIZE
    insert_byte = []
    loop = 3
    
    for i in xrange(ELF_SIZE - num - 1):
        insert_byte.append(0)
    for i in xrange(loop):
        for i in xrange(ELF_SIZE):
            insert_byte.append(0)
    return insert_byte


if __name__ == '__main__':
    # byte1: free,  byte2: syscall_hook.ko
    entry = np.loadtxt(sys.argv[1], delimiter=',', dtype='int')
    print("length of ep: {0}".format(len(entry)))
    file1 = raw_input('file1: ')
    f1 = open(file1, "rb")
    file2 = raw_input('file2: ')
    f2 = open(file2, "rb")
    data1 = f1.read()
    data2 = f2.read()
    byte1, byte2 = [], []
    # cutting_header2 = []
       
    for i in xrange(len(data1)):
        byte1.append(ord(data1[i]))
    for i in xrange(len(data2)):
        byte2.append(ord(data2[i]))

    ep = 0
    for file_num in range(int(sys.argv[2]), int(sys.argv[2]) + FILE_NUM):
        if ep > len(entry):
            print("No more entry!")
            break
        f = open("binary_%d" % file_num, "wb")
        connecting, cutting_header1 = [], [] 
        cutting_num = 0

        print("file_{0}:".format(file_num))

        # Insert header1
        # print("Insert header1...")
        cutting_header1 = cutting_header1_func(byte2)
        for i in xrange(len(cutting_header1)):
            connecting.append(cutting_header1[i])

        # Insert cutting until over BYTE_SIZE
        while len(connecting) < BYTE_SIZE:
            cutting, inserting = [], []

            if (ep + 2) > len(entry):
                print("No more entry!")
                break
            if entry[ep+1] - entry[ep] > THRESHOLD:
                ep = ep + 2
                continue
            
            # print("cutting...")
            cutting = cutting_func(byte1, entry[ep], entry[ep+1])

            cutting_num = cutting_num + 1
            print("ep = {0}".format(ep))
            # print("connecting...")
            for i in xrange(len(cutting)):
                connecting.append(cutting[i])

            # Insert zero between functions
            # print("inserting zero...")
            inserting = insert_zero(len(connecting) - 1)
            for i in xrange(len(inserting)):
                connecting.append(inserting[i])
            ep = ep + 2

        print("cutting_num = {0}, total_byte = {1}"
              .format(cutting_num, len(connecting)))
        if len(connecting) == 112:
            sys.exit(main())

        # Insert zero until file size is FILE_BYTE
        if len(connecting) > FILE_BYTE:
            print("Over FILE_BYTE size!")
        else:
            for i in xrange(FILE_BYTE - len(connecting)):
                connecting.append(0)

        print("connecting size = {0}".format(len(connecting)))
        # Write connecting to binary_file
        for item in connecting:
            f.write(struct.pack("B", item))
        f.close()
        
        # print("header2...")
        # cutting_header2 = cutting_header2_func(byte2)            
        # for i in xrange(len(cutting_header2)):
        #     connecting.append(cutting_header2[i])
    
    f1.close()
    f2.close()
    
