from codons.codons import codonTableBaseT as table
import itertools

newtable = []
for i in table:
    for j in table[i]:
        newtable.append(j)

combinations = list(itertools.product(newtable, newtable))

for i in combinations:
    count = 0
    for j in combinations:

        if i == j:
            count += 1
    if count > 1:
        print("{} has count: {}".format(i.count))
        break
print(newtable, len(newtable))
print(len(combinations))
