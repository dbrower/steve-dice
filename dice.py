#!/usr/bin/python

import random
import math

# 6=two successes
# 5=one success
# 4=non success (but has some value as a mojo shard)
# 3-you MAY reroll die + one other die (but don't have to)
# 2-you MAY add one dice to the mix. (Maximum of 7 die total)
# 1-one failure


def eval_die(n):
    if n == 6:
        return 2
    elif n == 5:
        return 1
    elif n == 1:
        return -1
    return 0

class State:
    def __init__(self):
        self.dice = [0]*7
        self.active_two = []
        self.active_three = []

    def __str__(self):
        return "Dice {} / {}".format(self.dice, self.active_three)

    def eval(self):
        return sum([eval_die(n) for n in self.dice])

    def roll(self, n):
        # roll the first n dice
        self.dice = [0]*7
        self.active_two = []
        self.active_three = []
        for i in range(n):
            self.dice[i] = random.randint(1,6)
            if self.dice[i] == 2:
                self.active_two.append(i)
            elif self.dice[i] == 3:
                self.active_three.append(i)

    def reroll(self, strat_f):
        if not strat_f:
            strat_f = self.find_matching
        # the set of indicies that are being rerolled
        reroll_choices = []
        # figure out rerolls
        for i in self.active_two:
            if 0 in self.dice and strat_f([], 1) >= 0:
                j = self.dice.index(0)
                self.dice[j] = -1
                reroll_choices.append(j)
        # now reroll any active 3s
        for i in self.active_three:
            n = strat_f([i] + reroll_choices, 0)
            if n > -1:
                reroll_choices.append(i)
                reroll_choices.append(n)
            elif n == -1:
                # just reroll the 3 with no matching die
                reroll_choices.append(i)
        #print "---> {} = {}".format(self.dice, self.eval())
        #print "Reroll {}".format(reroll_choices)
        self.active_two = []
        self.active_three = []
        for i in reroll_choices:
            self.dice[i] = random.randint(1,6)
            if self.dice[i] == 2:
                self.active_two.append(i)
            elif self.dice[i] == 3:
                self.active_three.append(i)
        return len(reroll_choices) > 0

    def find_all(self, n):
        return [i for i in range(len(self.dice)) if self.dice[i] == n]

    # returns:
    #  >= 0 = index of other die to reroll
    #  -1   = no matching die, just reroll the 3
    #  -2   = don't reroll the 3
    def find_matching(self, reroll_choices, switch):
        # switch is a hack...if 1 it means decide whether
        # to reroll a 2. 0 = yes, <0 = no
        if switch == 1:
            # always add more dice
            return 0
        # we choose to reroll dice in the following order:
        #  first any 1s
        #  then any 2s
        #  then any 4s
        # the goal is to maximize points.
        for i in self.find_all(1):
            if i not in reroll_choices:
                return i
        for i in self.find_all(2):
            if i not in reroll_choices:
                return i
        for i in self.find_all(4):
            if i not in reroll_choices:
                return i
        return -1

    def find_matching_strategy_three(self, reroll_choices, switch):
        # find a reroll die in the following order:
        #  if the value of the dice is >= 3 then don't do anything
        # otherwise,
        #  first any 1s
        #  then any 2s
        #  then any 4s
        if self.eval() >= 3:
            return -2
        return self.find_matching(reroll_choices, switch)

    def find_matching_strategy_four(self, reroll_choices, switch):
        if self.eval() >= 4:
            return -2
        return self.find_matching(reroll_choices, switch)



def histo(lst,n):
    counts = {}
    nn = float(n)
    for i in lst:
        counts[i] = counts.get(i, 0) + 1
    ks = counts.keys()
    ks.sort()
    for k in ks:
        print "%8d %8d %8f" % (k, counts[k], counts[k]/nn)

def mean_stddev(lst):
    n = len(lst)
    s = sum(lst)
    m = float(s)/n
    ss = sum(( (x-m)**2 for x in lst))
    v = float(ss)/(n-1)
    return m, v

def stats(n, ndice):
    outcomes = []
    num_rolls = []
    dice = State()
    for i in range(n):
        roll_count = 1
        dice.roll(ndice)
        while dice.reroll(dice.find_matching_strategy_three):
            roll_count += 1

        num_rolls.append(roll_count)
        outcomes.append(dice.eval())

    #     "-------- -------- --------"
    print ndice,"Dice, n=",n,"trials"
    print "outcome  count    prob"
    histo(outcomes, n)
    m, v = mean_stddev(outcomes)
    # compute sample error
    print "expected return", m, 2*math.sqrt(v/n)
    print "expected std dev", v
    print "rolls    count    prob"
    histo(num_rolls, n)
    m, v = mean_stddev(num_rolls)
    print "avg rolls", m, 2*math.sqrt(v/n)
    print "expected variance", v

for d in range(2,7):
    stats(100000, d)
