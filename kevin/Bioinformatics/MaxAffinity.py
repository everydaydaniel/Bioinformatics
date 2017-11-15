import analysis.getAfinityValues as afinity
import sequencing.acidToDNA as acidToDNA
import random
lookup = afinity.mfeDictionary

'''This code will break up the imput sequence into synonymous codons and
generates 3 sequence trains: 1. wt, 2.high, and 3. random. In this way, a
random guided walk towards achieving the highest affinity variant of the imput
sequence is achieved.
'''

#sequence = sequenceReading.readFile("ATGGCCGACTACAAGTGATAA")
sequence = acidToDNA.swapBase("ATGGCCGACTACAAGGACGATGACGACAAGGGAGGATCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCCATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTGAGCTACCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGGAGCTCCATCATCATCATCATCACAGCAGCGGCCTGGTGCCGCGCGGCAGCCATGAATTCGGATCCGCTGGCTCCGCTGCTGGTTCTGGCGTCGACATGAGTGGAATACTGACGCGCTGGCGACAGTTTGGTAAACGCTACTTCTGGCCGCATCTCTTATTAGGGATGGTTGCGGCGAGTTTAGGTTTGCCTGCGCTCAGCAACGCCGCCGAACCAAACGCGCCCGCAAAAGCGACAACCCGCAACCACGAGCCTTCAGCCAAAGTTAACTTTGGTCAATTGGCCTTGCTGGAAGCGAACACACGCCGCCCGAATTCGAACTATTCCGTTGATTACTGGCATCAACATGCCATTCGCACGGTAATCCGTCATCTTTCTTTCGCAATGGCACCGCAAACACTGCCCGTTGCTGAAGAATCTTTGCCTCTTCAGGCGCAACATCTTGCATTACTGGATACGCTCAGCGCGCTGCTGACCCAGGAAAGGCACGCCGTCTGA","U")
pos = 0
WTsequence = ""
HIsequence = ""
RNDsequence = ""
WTaff = 0
HIaff = 0
RNDaff = 0
#while you're one codon away from the stop codon, generate all combinations and
#add them to the corresponding  WT, HI, or RND sequence, also store the affinity values
while pos < len(sequence)-6:
    codon1 = sequence[pos:pos+3]
    codon2 = sequence[pos+3:pos+6]


    allpos = acidToDNA.CreateSixMer(codon1+codon2)
    aList = []
    for i in allpos:
        aList.append(lookup[i])


    #for the wildtype sequence
    WTsequence += codon1
    WTaff += aList[0]
    #for the Maximum affinity sequence
    indOfHI = aList.index(min(aList))
    HIsequence += allpos[indOfHI][0:3]
    HIaff += aList[indOfHI]

    #for the random sequence
    indOfRND = random.randrange(0,len(aList))
    RNDsequence += allpos[indOfRND][0:3]
    RNDaff += aList[indOfRND]


    pos += 3

#add the second to last codon and stop codon
#for wildtype
WTsequence += codon2 + sequence[pos+3:pos+6]
HIsequence += allpos[indOfHI][3:6] + sequence[pos+3:pos+6]
RNDsequence += allpos[indOfRND][3:6] + sequence[pos+3:pos+6]

#Calculate Affinity
def CalculateAffinity(sequence):
    sequence = acidToDNA.swapBase(sequence,"U")
    pos = 0
    aff = 0
    while pos < len(sequence)-6:
        codons = sequence[pos:pos+6]
        aff += lookup[codons]

        pos += 3
    return aff

affWT = CalculateAffinity(WTsequence)
affHI = CalculateAffinity(HIsequence)
affRND =CalculateAffinity(RNDsequence)

#rewrite to T instead of U
print(acidToDNA.swapBase(WTsequence), "affinityWT:", WTaff)
print(acidToDNA.swapBase(HIsequence),"affinityHI:", HIaff)
print(acidToDNA.swapBase(RNDsequence),"affinityRND:", RNDaff)
print(acidToDNA.swapBase(WTsequence), "affinityCalculatedWT:", affWT)
print(acidToDNA.swapBase(HIsequence),"affinityCalculatedHI:", affHI)
print(acidToDNA.swapBase(RNDsequence),"affinityCalculatedRND:", affRND)
print(sequence)




'''
aa1 = sequence[0:3]
aa2 = sequence[3:6]

allpos = acidToDNA.CreateSixMer(aa1+aa2)
print("These are all of the possibilities: ", allpos)
aList = []

for i in allpos:
    print(lookup[i])
    aList.append(lookup[i])

indOfMax = aList.index(max(aList))
#if len(allpos) >
#indOfRand =



print("Affinity Values: ", aList)

print(allpos[indOfMax][3:6])
print("index of max", indOfMax)
print(aList[1])
'''
