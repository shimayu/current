# Usage #
# python connecting_byte.py 

import sys
import pickle
import struct

ELF_size = 16

def cutting_func(byte, start, end):
    cutting = []

    print("start_byte_locate: byte[{0}] = 0x{1}"
          .format(start, hex(byte[start])))
    print("end_byte_locate: byte[{0}] = 0x{1}"
          .format(end, hex(byte[end])))

    for i in range(start, end + 1):
        cutting.append(byte[i])

    # for i in xrange(len(cutting)):
    #     print("cutting[{0}] = 0x{1}".format(i, hex(cutting[i])))

    return cutting

def cutting_header1_func(byte):
    cutting_header1 = []

    for i in xrange(112):
        cutting_header1.append(byte[i])

    return cutting_header1

# def cutting_mal_func(byte):
#     cutting_mal = []

#     for i in range(112, 351+1):
#         cutting_mal.append(byte[i])

#     return cutting_mal

# def cutting_header2_func(byte):
#     cutting_header2 = []

#     for i in range(360, len(byte)):
#         cutting_header2.append(byte[i])

#     return cutting_header2

def insert_zero(index):
    num = index % ELF_size
    insert_byte = []
    
    for i in xrange(ELF_size - num - 1):
        insert_byte.append(0)

    loop = 3
    for i in xrange(loop):
        for i in xrange(ELF_size):
            insert_byte.append(0)

    return insert_byte


if __name__ == '__main__':
    # byte1: free,  byte2: syscall_hook.ko
    entry = [64, 175, 207, 511, 719, 847, 943, 1055, 1199, 1231, 1407,
             1503, 1535, 1567, 1647, 1967, 2095, 2159, 2447, 2591, 2671]

    file1 = raw_input('file1: ')
    f1 = open(file1, "rb")
    file2 = raw_input('file2: ')
    f2 = open(file2, "rb")
    data1 = f1.read()
    data2 = f2.read()
    byte1 = []
    byte2 = []

    cutting_header2 = []

    
    
    for i in xrange(len(data1)):
        byte1.append(ord(data1[i]))
    for i in xrange(len(data2)):
        byte2.append(ord(data2[i]))

    ep = 0

    for file_num in xrange(1):
        f = open("binary_%d" % file_num, "wb")
        connecting = []
        cutting_header1 = []
        
        print("Insert header1...")
        cutting_header1 = cutting_header1_func(byte2)
        for i in xrange(len(cutting_header1)):
            connecting.append(cutting_header1[i])
    
        while len(connecting) < 600:
            cutting = []
            inserting = []
            
            print("cutting...")
            if ep == 0:
                cutting = cutting_func(byte1, entry[ep], entry[ep+1])
            else:
                cutting = cutting_func(byte1, entry[ep] + 1, entry[ep+1])
            print("connecting...")
            for i in xrange(len(cutting)):
                connecting.append(cutting[i])
            print("inserting zero...")
            inserting = insert_zero(len(connecting) - 1)
            for i in xrange(len(inserting)):
                connecting.append(inserting[i])

            ep = ep + 1

        # for i in xrange(len(connecting)):
        #     print("{0}: 0x{1}".format(i, hex(connecting[i])))

        print("type of item = {0}".format(type(connecting[0])))
        for item in connecting:
            print("item = %s", hex(item))
            f.write(struct.pack("B", item))
        # pickle.dump(connecting, f)
        f.close()

    # print("cutting2...")
    # cutting2 = cutting_mal_func(byte2)
        
    # print("header2...")
    # cutting_header2 = cutting_header2_func(byte2)    

        
    # for i in xrange(len(cutting_header2)):
    #     connecting.append(cutting_header2[i])


    # for i in xrange(len(connecting)):
    #     print("{0}: 0x{1}".format(i, hex(connecting[i])))
    
    f1.close()
    f2.close()
    
