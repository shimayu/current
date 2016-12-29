# Usage #
# python connecting_byte.py 

import numpy as np
import struct
import random

ELF_SIZE = 16
FILE_NUM = 5
FILE_BYTE = 1440
BYTE_SIZE = 700
THRESHOLD = 600
HEADER1_LOCATE = 112
END_OF_MAL = 351

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

def cutting_mal_func(byte):
    cutting_mal = []

    for i in range(HEADER1_LOCATE, END_OF_MAL + 1):
        cutting_mal.append(byte[i])
    return cutting_mal

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
    entry = np.loadtxt('data_kallsyms.csv', delimiter=',', dtype='int')
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

    ep = 0  # entry pointer, common in all files 
    for file_num in xrange(FILE_NUM):
        if ep > len(entry):
            print("No more entry!")
            break
        f = open("binary_%d" % file_num, "wb")
        connecting, output, locate = [], [], []
        cutting_header1, cutting_mal = [], []
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

            locate.append(len(connecting))
            ep = ep + 2

        print("cutting_num = {0}, total_byte = {1}"
              .format(cutting_num, len(connecting)))

        # Insert mal_code into random locate between functions
        print("Inserting mal_code...")
        if cutting_num == 2:
            mal_locate = 0
        else:
            mal_locate = random.randint(0, cutting_num-2)
        cutting_mal = cutting_mal_func(byte2)
        for i in xrange(ELF_SIZE*3):
            cutting_mal.append(0)

        for i in xrange(locate[mal_locate]):
            output.append(connecting[i])
        for i in xrange(len(cutting_mal)):
            output.append(cutting_mal[i])
        for i in range(locate[mal_locate], len(connecting)):
            output.append(connecting[i])

        # Insert zero until file size is FILE_BYTE
        if len(output) > FILE_BYTE:
            print("Over FILE_BYTE size!")
        else:
            for i in xrange(FILE_BYTE - len(output)):
                output.append(0)            
        print("output size = {0}".format(len(output)))
        # Write output to binary_file
        for item in output:
            f.write(struct.pack("B", item))
        f.close()
        
        # print("header2...")
        # cutting_header2 = cutting_header2_func(byte2)            
        # for i in xrange(len(cutting_header2)):
        #     connecting.append(cutting_header2[i])
    
    f1.close()
    f2.close()
    
