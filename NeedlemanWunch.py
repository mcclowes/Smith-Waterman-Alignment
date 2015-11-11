#!/usr/bin/python

import sys

class NeedlemanWunch:
    def __init__(self, sA, sB, i, d, s, m):
        self.sequenceA = sA
        self.sequenceB = sB
        self.insert = i
        self.delete = d
        self.substitution = s
        self.match = m
        
        self.opt = [[0 for x in range(len(self.sequenceB)+1)] for x in range(len(self.sequenceA)+1)]
        self.dir = [[0 for x in range(len(self.sequenceB)+1)] for x in range(len(self.sequenceA)+1)]

#       // The allowed directions
        self.LEFT = 1
        self.DIAGONAL = 2
        self.UP = 4

    def align(self):
#       // First of all, compute insertions and deletions at 1st row/column
        self.opt[0][0] = 0
        for i in range (1, len(self.sequenceA)+1):
            self.opt[i][0] = self.opt[i - 1][0] + self.delete;
        for j in range (1, len(self.sequenceB)+1):
            self.opt[0][j] = self.opt[0][j - 1] + self.insert;

#       // Set the values of row 0 and column 0
        self.dir[0][0] = 2;
        for i in range(1, len(self.sequenceA)+1):
            self.dir[i][0] = 4
        
        for i in range(1, len(self.sequenceB)+1):
            self.dir[0][i] = 1

#       // Now compute the rest of the cells
        for i in range (1, len(self.sequenceA)+1):
            for j in range (1, len(self.sequenceB)+1):
                scoreDiag = self.opt[i - 1][j - 1]
                if (self.sequenceA[i-1] == self.sequenceB[j-1]):
                    scoreDiag += self.match
                else:
                    scoreDiag += self.substitution
                scoreLeft = self.opt[i][j - 1] + self.insert
                scoreUp = self.opt[i - 1][j] + self.delete
#               // we take the minimum
                self.opt[i][j] = min(scoreDiag, scoreLeft, scoreUp)
                self.dir[i][j] = 0
                if (self.opt[i][j] == scoreLeft):
                    self.dir[i][j] += self.LEFT
                if (self.opt[i][j] == scoreDiag):
                    self.dir[i][j] += self.DIAGONAL
                if (self.opt[i][j] == scoreUp):
                    self.dir[i][j] += self.UP
#       // end of align

    def outputMatrices(self):
        for j in range (-1, len(self.sequenceB)+1):
            if (j >= 1):
                print(self.sequenceB[j-1] + '\t'),
            else:
                print('\t'),
        print
        for i in range (0, len(self.sequenceA)+1):
            if (i >= 1):
                print(self.sequenceA[i-1] + '\t'),
            else:
                print('\t'),
            for j in range(0, len(self.sequenceB)+1):
                print(str(self.opt[i][j]) + '\t'),
            print
        print

        for j in range (-1, len(self.sequenceB)+1):
            if (j >= 1):
                print(self.sequenceB[j-1] + '\t'),
            else:
                print('\t'),
        print
        # Output directions
    
        for i in range (0, len(self.sequenceA)+1):
            if (i >= 1):
                print(self.sequenceA[i-1] + '\t'),
            else:
                print('\t'),
            for j in range(0, len(self.sequenceB)+1):
                print(str(self.dir[i][j]) + '\t'),
            print
#       // end of output matrix

    def recurseTree(self, d, a, tailTop, tailBottom):
        if (d == 0 and a == 0):
            print("+")
            print(tailTop)
            print(tailBottom)
        else:
            tc = ''
            if (d >= 0):
                tc = self.sequenceA[d-1]
            bc = ''
            if (a >= 0):
                bc = self.sequenceB[a-1]

            if ((self.dir[d][a] & self.LEFT) == self.LEFT): # we go left
                self.recurseTree(d, a - 1, '-' + tailTop, bc + tailBottom)

            if ((self.dir[d][a] & self.DIAGONAL) == self.DIAGONAL): # we go diagonal
                self.recurseTree(d - 1, a - 1, tc + tailTop, bc + tailBottom)

            if ((self.dir[d][a] & self.UP) == self.UP): # we go up
                self.recurseTree(d - 1, a, tc + tailTop, '-' + tailBottom)
#       // end of recurse tree

    def outputAlignments(self):
        self.recurseTree(len(self.sequenceA), len(self.sequenceB), '', '')

# The main code:

with open(sys.argv[1]) as f:
    sA = f.readline().rstrip()
    sB = f.readline().rstrip()

print sA
print sB

nw = NeedlemanWunch(sA, sB, 1, 1, 1, 0)
nw.align()
nw.outputMatrices()
nw.outputAlignments()

