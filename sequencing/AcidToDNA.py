from codons.codons import codonTableBaseT, codonTableBaseU

# read in a sequence, make sure it is uppercase and whitespace stripped
# TODO: Ask keven if files come in formated: they do!


def readSequence(sequence):
    sequence = sequence.strip().upper()
    return sequence

# Swap T to U and vise versa if needed


def swapBase(sequence, toSwap="U"):
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
    assigned = 0
    for i in codonTable:
        if assigned == 2:
            break
        if startCodons[0] in codonTable[i]:
            amino1[i] = codonTable[i]
            assigned += 1
        elif startCodons[1] in codonTable[i]:
            amino2[i] = codonTable[i]
            assigned += 1
    return amino1, amino2

# return the value in a output file


def CreateSixMer(sequence):
    pass


if __name__ == '__main__':
    s = "AUU"
    t = "ATTACG"
    s = readSequence(s)
    print(getTableIdx(t))
