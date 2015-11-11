#!/usr/bin/python

import sys

class SmithWaterman:
    def __init__(self, sA, sB, i, d, s, m):
        self.sequenceA = sA
        self.sequenceB = sB
        self.insert = i
        self.delete = d
        self.substitution = s
        self.match = m

        self.alignments = []
        
        self.opt = [[0 for x in range(len(self.sequenceB)+1)] for x in range(len(self.sequenceA)+1)]
        self.dir = [[0 for x in range(len(self.sequenceB)+1)] for x in range(len(self.sequenceA)+1)]

        # The allowed directions
        self.LEFT = 1
        self.DIAGONAL = 2
        self.UP = 4
        self.JUMP = 8

    def align(self):
        # First of all, compute insertions and deletions at 1st row/column
        self.opt[0][0] = 0
        for i in range (1, len(self.sequenceA)+1):
            self.opt[i][0] = 0
        for j in range (1, len(self.sequenceB)+1):
            self.opt[0][j] = 0

        # Set the values of row 0 and column 0
        self.dir[0][0] = 0;
        for i in range(1, len(self.sequenceA)+1):
            self.dir[i][0] = 8
        for i in range(1, len(self.sequenceB)+1):
            self.dir[0][i] = 8

        # Now compute the rest of the cells
        for i in range (1, len(self.sequenceA)+1):
            for j in range (1, len(self.sequenceB)+1):
                scoreDiag = self.opt[i - 1][j - 1]
                if (self.sequenceA[i-1] == self.sequenceB[j-1]):
                    scoreDiag += self.match
                else:
                    scoreDiag += self.substitution
                scoreLeft = self.opt[i][j - 1] + self.insert 
                scoreUp = self.opt[i - 1][j] + self.delete

                # we take the maximum
                self.opt[i][j] = max(0, scoreDiag, scoreLeft, scoreUp)
                self.dir[i][j] = 0

                if (self.opt[i][j] == scoreLeft): # Left is max and not 0
                    self.dir[i][j] += self.LEFT
                if (self.opt[i][j] == scoreDiag): # Diagonal is max and not 0
                    self.dir[i][j] += self.DIAGONAL
                if (self.opt[i][j] == scoreUp): # Diagonal is max and not 0
                    self.dir[i][j] += self.UP
                if (self.opt[i][j] == 0):
                    self.dir[i][j] += self.JUMP
                # end of align

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
        # end of output matrix

    def recurseTree(self, d, a, tailTop, tailBottom):
        if ((d == 0 and a == 0)):
            finalA = tailTop
            finalB = tailBottom

            # Pad strings
            while (len(finalA) < len(finalB)):
                finalA = '-' + finalA
            while (len(finalA) > len(finalB)):
                finalB = '-' + finalB

            finalA = list(finalA)
            finalB = list(finalB)

            # Create alignment visualisation
            for i in range(len(finalA)):
                if (finalA[i] != finalB[i]):
                    finalA[i] = finalA[i].lower()
                    finalB[i] = finalB[i].lower()

            finalA = ''.join(finalA)
            finalB = ''.join(finalB)

            #Print alignment
            #print finalA
            #print finalB

            self.alignments.append(finalB)

            return
        else:
            tc = ''
            if (d >= 0):
                tc = self.sequenceA[d-1]

            bc = ''
            if (a >= 0):
                bc = self.sequenceB[a-1]

            # Finished local alignment
            if ((self.dir[d][a] & self.JUMP) == self.JUMP):
                restofA = (self.sequenceA[0:d])
                restofB = (self.sequenceB[0:a])
                self.recurseTree(0, 0, restofA + tailTop, restofB + tailBottom)
                return

            #Should this be elsed?
            if ((self.dir[d][a] & self.LEFT) == self.LEFT): # Left
                self.recurseTree(d, a - 1, '-' + tailTop, bc + tailBottom)
            
            if ((self.dir[d][a] & self.DIAGONAL) == self.DIAGONAL): # Diagonal
                self.recurseTree(d - 1, a - 1, tc + tailTop, bc + tailBottom)
            
            if ((self.dir[d][a] & self.UP) == self.UP): # Right
                self.recurseTree(d - 1, a, tc + tailTop, '-' + tailBottom)

        # end of recurse tree

    def outputAlignments(self):
        maxval, i, j = max((item, i, j)  for i, row in enumerate(self.opt) for j, item in enumerate(row))

        for i in range(len(self.sequenceA)+1)[-1::-1]:
            for j in range(len(self.sequenceB)+1)[-1::-1]:
                if (self.opt[i][j] == maxval):
                    # print('found at: (' + str(i) + ', ' + str(j) + ').')
                    restofA = self.sequenceA[i:]
                    restofB = self.sequenceB[j:]

                    # Pad tail
                    while (len(restofA) < len(restofB)):
                        restofA = restofA + '-'
                    while (len(restofA) > len(restofB)):
                        restofB = restofB + '-'

                    #Begin local alignment
                    self.recurseTree(i, j, restofA, restofB) #(including the rest of the genome around it)

        return self.alignments

#merges sequence2 onto the end of sequence1
def mergeSequences(sequence1, sequence2):
    for i in range(min(len(sequence1), len(sequence2))):
        # print 'a > ' + str(sequence1[i + (len(sequence1) - min(len(sequence1), len(sequence2))):]) + ', b > ' + str(sequence2[:- (len(sequence2) - min(len(sequence1), len(sequence2))) - i ])
        if sequence1[i + (len(sequence1) - min(len(sequence1), len(sequence2))):] == sequence2[:- (len(sequence2) - min(len(sequence1), len(sequence2))) - i ]:
            # print 'merging ' + str(sequence2[- (len(sequence2) - min(len(sequence1), len(sequence2))) - i:])
            return sequence1 + sequence2[- (len(sequence2) - min(len(sequence1), len(sequence2))) - i:]
    # print 'flat merging ' + str(sequence1 + sequence2)
    return sequence1 + sequence2

# The main code:

# Read in file
with open(sys.argv[1]) as f:
    sequences = f.readlines()

#Print template sequence and other sequences
print ('\nTemplate sequence: ' + sequences[0].rstrip())
for i in range(len(sequences))[1:]:
    if (str(sequences[i]) == '\n'): # Check for new lines
        del sequences[i]
        continue
    print ('Sequence ' + str(i) + ': ' + sequences[i].rstrip())
print '\n',

# Locally align...
print sequences[0].rstrip()
allAlignments = []

for i in range(len(sequences))[1:]:
    nw = SmithWaterman(sequences[0].rstrip(), sequences[i].rstrip(), -1, -1, -3, 1) # Alter these parameters to change scoring schema
    nw.align()
    #nw.outputMatrices()
    allAlignments.extend(nw.outputAlignments())

# ... and remove duplicates...
for i in range(len(allAlignments)):
    allAlignments[i] = (allAlignments[i].rstrip('-')).upper()
allAlignments = list(set(allAlignments))

# ... and sort and print
(allAlignments).sort(lambda x, y: cmp(x.count('-'), y.count('-')))
for item in allAlignments:
    print item + '-' * (len(sequences[0]) - len(item) - 1)

# Merge local alignments
print ('\nTemplate sequence:\t' + sequences[0].rstrip()),
print '\nNew sequence:\t\t',
mergedSequence = list(allAlignments[0].strip('-')) #put first sequence as starting point, removing indels
for i in range(1,len(allAlignments)):
    targetSequence = list(allAlignments[i].strip('-'))
    # print mergedSequence
    mergedSequence = mergeSequences(mergedSequence, targetSequence)

# print sequences[0],
# print mergedSequence
print (''.join(mergedSequence)).upper()
