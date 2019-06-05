from collections import defaultdict


index = 10
N = 1
sentence = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
prefix = sentence[index - N + 1:index]

print(len(prefix))
print (prefix)

bigramCounter = defaultdict(float)
bigramCounter[('a','b')] = 5
bigramCounter[('a','c')] = 56
bigramCounter[('a','d')] = 7

reduced_d = {(lw, w): v for (lw, w), v in bigramCounter.items() if lw != 'a'}
print(reduced_d)
if reduced_d:
    print("ohno")
for (x,y) in reduced_d.keys():
    print("ohno")

mu = 0.01
print((45 + mu) / (400 + 51150 * mu))
mu = 1.0
print((45 + mu) / (400 + 51150 * mu))
print(45.0/400)