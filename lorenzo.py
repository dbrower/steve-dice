#!/usr/bin/python

import random


# n = amount in center
# return new amount in center
def roll(n):
    is_double = True
    while is_double:
        die1 = random.randint(1,6)
        die2 = random.randint(1,6)
        #print "n=",n
        #print "roll",die1,die2

        # first calculate change of center pile
        if die1 == 5:
            n += 1
        if die2 == 5:
            n += 1
        if die1 == 2:
            if n > 0:
                n -= 1
        if die2 == 2:
            if n > 0:
                n -= 1

        is_double = (die1 == die2)
    #print "n=",n
    return n

def histo(lst,n):
    counts = {}
    nn = float(n)
    for i in lst:
        counts[i] = counts.get(i, 0) + 1
    ks = counts.keys()
    ks.sort()
    for k in ks:
        print "%8d %8d %8f" % (k, counts[k], counts[k]/nn)


for start in range(7):
    result = []
    count = 100000
    for i in range(count):
        # assume 4 playing
        n = roll(roll(roll(roll(start))))
        result.append(n)

    print "starting at",start
    histo(result,count)
