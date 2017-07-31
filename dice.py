#!/usr/bin/python

import random

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
        self.active_three = []

    def __str__(self):
        return "Dice {} / {}".format(self.dice, self.active_three)

    def eval(self):
        return sum([eval_die(n) for n in self.dice])

    def roll(self, n):
        # roll the first n dice
        self.dice = [0]*7
        self.active_three = []
        num_twos = 0
        for i in range(n):
            self.dice[i] = random.randint(1,6)
            if self.dice[i] == 2:
                num_twos += 1
            elif self.dice[i] == 3:
                self.active_three.append(i)
        for n in range(num_twos):
            if 0 in self.dice:
                self.dice[self.dice.index(0)] = -1

    def reroll(self):
        # the set of indicies that are being rerolled
        reroll_choices = []
        # dice which have been added are marked as -1
        num_negone = self.find_all(-1)
        reroll_choices.extend(num_negone)
        # now reroll any active 3s
        for i in self.active_three:
            n = self.find_matching_strategy_four([i] + reroll_choices)
            if n > -1:
                reroll_choices.append(i)
                reroll_choices.append(n)
        #print "Reroll {}".format(reroll_choices)
        self.active_three = []
        for i in reroll_choices:
            self.dice[i] = random.randint(1,6)
            if self.dice[i] == 2:
                if 0 in self.dice:
                    self.dice[self.dice.index(0)] = -1
            elif self.dice[i] == 3:
                self.active_three.append(i)
        return len(reroll_choices) > 0

    def find_all(self, n):
        return [i for i in range(len(self.dice)) if self.dice[i] == n]

    def find_matching(self, reroll_choices):
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

    def find_matching_strategy_three(self, reroll_choices):
        # find a reroll die in the following order:
        #  if the value of the dice is >= 3 then don't do anything
        # otherwise,
        #  first any 1s
        #  then any 2s
        #  then any 4s
        if self.eval() >= 3:
            return -1
        return self.find_matching(reroll_choices)

    def find_matching_strategy_four(self, reroll_choices):
        if self.eval() >= 4:
            return -1
        return self.find_matching(reroll_choices)



def histo(lst,n):
    counts = {}
    nn = float(n)
    for i in lst:
        if i in counts:
            counts[i] += 1
        else:
            counts[i] = 1
    ks = counts.keys()
    ks.sort()
    for k in ks:
        print "%8d %8d %8f" % (k, counts[k], counts[k]/nn)

def stats(n, ndice):
    outcomes = []
    num_rolls = []
    dice = State()
    for i in range(n):
        roll_count = 1
        dice.roll(ndice)
        while dice.reroll():
            roll_count += 1

        num_rolls.append(roll_count)
        outcomes.append(dice.eval())

    print "outcomes"
    histo(outcomes, n)
    print "rolls"
    histo(num_rolls, n)
    print "avg rolls", float(sum(num_rolls))/n


stats(10000, 4)
