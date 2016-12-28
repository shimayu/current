import numpy as np
import sys

data = np.loadtxt(sys.argv[1], delimiter=',', dtype='int')
diff, byte_diff, one_diff = [], [], []

print("length of data: {0}".format(len(data)))

for i in xrange(len(data)):
    print("data[{0}]: {1}".format(i, data[i]))

for i in xrange(len(data) - 1):
    diff.append(data[i+1] - data[i])
    print("diff[{0}]: {1}".format(i, diff[i]))

for i in xrange(len(diff)):
    if i % 2 == 0:
        byte_diff.append(diff[i])
    else:
        one_diff.append(diff[i])

print("Check the difference of next byte is 1 or not")
for i in xrange(len(one_diff)):
    print("one_diff[{0}]: {1}".format(i, one_diff[i]))

print("difference of next byte...")
for i in xrange(len(byte_diff)):
    print("byte_diff[{0}]: {1}".format(i, byte_diff[i]))
    

