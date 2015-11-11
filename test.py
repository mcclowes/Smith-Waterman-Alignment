test = [['-', '-', 1,2,3,4, '-', '-', '-', '-'],[3,4,5,6,6,7,7],[1,2]]

test.sort(lambda x,y: cmp(len(filter(lambda a: a != '-', x)), len(filter(lambda a: a != '-', y))))

print test

print test.sort(lambda x, y: cmp(len(str(x).lstrip('-')), len(str(y).lstrip('-'))))

print str(test[2]).strip('\'-\'')

#filter(lambda a: a != '-', test[2])