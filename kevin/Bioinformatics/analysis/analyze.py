# simple calculations are defined in this module.


def deltaDiff(wildType, current):
    return abs(wildType - current)


def energyDiff(wildType, current):
    return current - wildType


# filter out values and return those that have the max aboslute
# energy difference
# ex: input = ("sequence", deltadiff, energyDiff)
# input: ('CAAAAG', 1.1, 1.1), ('CAGAAA', 2.9, 2.9), ('CAGAAG', 2.9, 2.9)
# returns: ('CAGAAA', 2.9, 2.9), ('CAGAAG', 2.9, 2.9)
def getEnergyDiff(setOfValues):
    absoluteValues = [abs(value[-1]) for value in setOfValues]
    max_value = max(absoluteValues)
    indexs = [i for i in range(len(absoluteValues)) if absoluteValues[i] == max_value]
    max_energydiffValues = [setOfValues[i] for i in indexs]
    return max_energydiffValues


# returns sequence max delta diff value and max energyDiff values
# we take the wildtype sequence so that we can compute the ebery/delta
# difference values
# wildType = wildTypeEnergy from mfe lookup table
# set of values = all different codon mutaions and they're mfe values
# returns: ((maxDeltaDiff), [max_energy_difference_values])
# (maxDeltaDiff) = (sequence, deltadiff, energydiff)
# [max_energy_difference_values] = [(sequence, delatadiff, energydiff)]
def get_energy_values(wildType, setOfValues):
    # all are positive values
    deltaDiff_values = []
    for values in setOfValues:
        sequence, current = values[0], values[1]
        deltaDiff_values.append((sequence, deltaDiff(wildType, current),
                                 energyDiff(wildType, current)))

    max_deltaDiff_value = max(deltaDiff_values, key=lambda x: x[1])
    max_energy_difference_values = getEnergyDiff(deltaDiff_values)
    # need this for get signs later, don't need the first value because it is not a mutation
    energy_difference_values = deltaDiff_values[1:]
    return (max_deltaDiff_value, max_energy_difference_values, energy_difference_values)


# this function will give us the number of positive, negative and zero values
# returns (positive, negative, zero)
def getSigns(setOfValues):
    positive, negative, zero = 0, 0, 0
    for value in setOfValues:
        if value[-1] == 0:
            zero += 1
        elif value[-1] > 0:
            positive += 1
        else:
            negative += 1
    return positive, negative, zero


def getSequenceString(sequences_with_max_energy, delimiter=";"):
    sequenceString = ''
    for sequence in sequences_with_max_energy:
        sequenceString += "{}{}".format(sequence, delimiter)
    return sequenceString
