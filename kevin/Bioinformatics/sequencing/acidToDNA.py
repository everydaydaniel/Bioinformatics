# from codons.codons import codonTableBaseT, codonTableBaseU
import pickle

# read in a sequence, make sure it is uppercase and whitespace stripped
# TODO: Ask keven if files come in formated: they do!


def createPickledDict(out_file, dict):
    with open("{}.pickle".format(out_file), 'wb') as outfile:
        pickle.dump(dict, outfile,  protocol=pickle.HIGHEST_PROTOCOL)


def createDict(pickleFile):
    with open(pickleFile, 'rb') as infile:
        return pickle.load(infile)


# Global creation of codon table
codonTableBaseT = createDict("codonTableBaseT.pickle")
codonTableBaseU = createDict("codonTableBaseU.pickle")


def readSequence(sequence):
    sequence = sequence.strip().upper()
    return sequence


# Need to check if a sequence contains a stop codon at the
# end
# input: sequence,
# keypair = [{'Q': ['CAA', 'CAG']}, {'K': ['AAA', 'AAG']}, 'Q', 'K']
def containsStopCodon(sequence, keyPair):
    # initialize stop codons
    stopCodons = ["UAA", 'UAG', 'UGA', 'TAA', 'TAG', 'TGA']
    codonPair = [sequence[:3], sequence[3:]]
    # this if check almost guarantees its a stop codon
    if codonPair[-1] in stopCodons and (keyPair[-1] is None):
        return True
    return False


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
def getTableIdx(sequence, base="U"):

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
def CreateSixMer(sequence, base="U"):
    # set original so that the first element in the list is
    # the original sequence
    original_sequence = sequence
    sequence = getTableIdx(sequence, base)

    if containsStopCodon(original_sequence, sequence):
        raise StopIteration

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


# takes in a seq and substitue the middle codon, the input should always be
# divisable by 3
# input is a len = 200-mer sequence but try to do for N-mer
# returns a list of sequences with the middle codon replaced
def substitue_N_Mer(sequence, base="U"):
    try:
        original_seq = sequence
        length = len(original_seq)
        insert_position = length // 2
        # slice the seq
        start, middle, end = original_seq[:insert_position - 3], original_seq[insert_position -3: insert_position], original_seq[insert_position:]
        # get the codon substitiutions
        codons_list = getTableIdx(middle)
        codons , key = codons_list[0], codons_list[-2]
        print(len(sequence))
        print(middle)
        # initialize data list
        sequences = [original_seq]
        for codon in codons[key]:
            # continue because we already added the original sequence
            if codon == middle:
                continue
            mutation_sequence = "{}{}{}".format(start, codon, end)
            sequences.append(mutation_sequence)

        return sequences


    except Exception as e:
        raise







if __name__ == '__main__':
    createPickledDict('codonTableBaseT', codonTableBaseT)
    createPickledDict('codonTableBaseU', codonTableBaseU)
    seq = substitue_N_Mer()
    print(seq)
    # s = "AUU"
    # t = "ATAACG"
    # s = readSequence(s)
    # t = readSequence(t)
    # two = getTableIdx(t)
    # print(t)
    # print(two)
else:
    createPickledDict('codonTableBaseT', codonTableBaseT)
    createPickledDict('codonTableBaseU', codonTableBaseU)
