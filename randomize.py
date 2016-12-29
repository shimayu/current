import numpy as np
import sys
import random

data1 = np.loadtxt(sys.argv[1], delimiter=',', dtype='int')

f1 = open(sys.argv[2], "w")

for i in xrange(len(data1)):
    f1.write(str(data1[i]))
    if i % 2 == 1 and i != (len(data1) - 1):
        f1.write(",")

for i in xrange(len(data1)):
    print("data1[{0}]: {1}".format(i, data1[i]))

f1.close()

data2 = np.loadtxt(sys.argv[2], delimiter=',', dtype='int')

f2 = open(sys.argv[2], "w")
random.shuffle(data2)

for i in xrange(len(data2)):
    print("data2[{0}]: {1}".format(i, data2[i]))

for i in xrange(len(data2)):
    f2.write(str(data2[i]))
    if i != (len(data2) - 1):
        f2.write(",")

f2.close()
