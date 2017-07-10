from codons.codons import codonTableBaseT, codonTableBaseU


# read in a sequence, make sure it is uppercase and whitespace stripped
# TODO: Ask keven if files come in formated: they do!


def readSequence(sequence):
    sequence = sequence.strip().upper()
    return sequence


# Swap T to U and vise versa if needed
def swapBase(sequence, toSwap="T"):
    toSwap = toSwap.upper()
    if toSwap == "T":
        return sequence.replace("U", "T")
    elif toSwap == "U":
        return sequence.replace("T", "U")
    else:
        return "Invalid toSwap: Use T or U"


# get the list of codons that make the protien
# sort it so that the input has the first pairs
# first. Assume you're given 6 codons.
# Sequence = sequence, Base: either T or U
# mer = number of codons. leave at 6 for now
# refactor later.
# Returns a dictionary of said pairs.
# Example:
# input: s = 'ATTACG'
# getTableIdx(s)
# output: [{'I': ['ATT', 'ATC', 'ATA']}, {'T': ['ACT', 'ACC', 'ACA', 'ACG']}]
def getTableIdx(sequence, base="T", mer=6):
    # Get codon table
    codonTable = None
    if base == "T":
        codonTable = codonTableBaseT
    else:
        codonTable = codonTableBaseU

    # Initialize variables
    startCodons = [sequence[:3], sequence[3:]]
    amino1, amino2 = {}, {}
    key1, key2 = None, None
    assigned = 0
    for i in codonTable:
        if assigned == 2:
            break
        if startCodons[0] in codonTable[i]:
            amino1[i] = codonTable[i]
            assigned += 1
            key1 = i
            if startCodons[1] in codonTable[i]:
                amino2[i] = codonTable[i]
                assigned += 1
                key2 = i
        elif startCodons[1] in codonTable[i]:
            amino2[i] = codonTable[i]
            assigned += 1
            key2 = i
            if startCodons[0] in codonTable[i]:
                amino1[i] = codonTable[i]
                assigned += 1
                key1 = i
    return [amino1, amino2, key1, key2]


# return the value in a output file
# Create a sixmer cross product
# input: a sequence of length 6
def CreateSixMer(sequence, base="T"):
    # set original so that the first element in the list is
    # the original sequence
    original_sequence = sequence
    sequence = getTableIdx(sequence, base)

    # get sets of codons
    list1, list2 = sequence[0][sequence[2]], sequence[1][sequence[-1]]
    cross = [original_sequence]
    # Cross product
    for i in list1:
        for j in list2:
            pair = i + j
            if pair == original_sequence:
                continue
            else:
                cross.append(pair)
    return cross


if __name__ == '__main__':

    seq = CreateSixMer("ACCACC")

    # s = "AUU"
    # t = "ATAACG"
    # s = readSequence(s)
    # t = readSequence(t)
    # two = getTableIdx(t)
    # print(t)
    # print(two)
