import csv
import re
import pickle
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib.font_manager import FontProperties
from math import isnan


# TODO: Remember to modularize this script
# TODO: Plot the data
# NOTE: You can yeild row results and preform operations on them
# NOTE: To import from a different script, from <script> (no ext) import * or function
# NOTE: Reference dict is a dict of dicts.


# Serialization functions
def toPickle(dictionary, outfile):
    with open("{}.pickle".format(outfile), 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()


def getPickle(infile):
    with open(infile, 'rb') as handle:
        return pickle.load(handle)


# Dictionary functions
def addToDict(key, aDict, ranges, sRNA=None, length=None, mRNA_map=None):
    # values are contained in a list to be able to add
    # multiple values to each key
    # store the length as a primary value since it would be redundandant
    # to store it for each key molecule
    # mRNA_map will be a tuple with the mRNA and the coreseponding range.
    # NOTE: ranges is a loop because string to list adds the lists in a list
    # sRNAs can have multiple interacting sites
    if key not in aDict:
        if not isinstance(length, int):
            raise Exception("Length is not an int.")
        aDict[key] = {"length": length, "sRNA": sRNA,
                      "mRNA": [mRNA_map], "ranges": [i for i in ranges]}
    else:
        # Error check sRNA
        if aDict[key]['sRNA'] != sRNA:
            # print(aDict[key]['sRNA'], sRNA)
            raise Exception("sRNA is different")
        for i in ranges:
            aDict[key]["ranges"].append(i)
        if mRNA_map not in aDict[key]["mRNA"]:
            aDict[key]["mRNA"].append(mRNA_map)


def addToRNADict(key, aDict, sRNA=None, sequence=None):
    # values are contained in a list to be able to add
    # multiple values to each key
    # store the length as a primary value since it would be redundandant
    # to store it for each key molecule
    if key not in aDict:
        aDict[key] = {"sequence": sequence, "sRNA": sRNA}
    else:
        # ERror check sRNA
        if aDict[key]['sRNA'] != sRNA:
            # print(aDict[key]['sRNA'], sRNA)
            raise Exception("sRNA is different")


def checkDictKey(key, dictionary):
    try:
        val = dictionary[key]
    except KeyError:
        return False
    return True


# String manipulation functions
# take in a string and convert it to a list object
def stringToList(string):
    # find matches inside two brackets [1,2], [3,2]
    # would find 1,2 3,2
    # returns a tuple of lists with ranges.
    try:
        matches = re.findall(r"\[(.*?)\]", string, re.IGNORECASE)
        list_of_lists = []
        for i in matches:
            list_of_lists.append(eval("[{}]".format(i)))
        multi_list = tuple(list_of_lists)
        return multi_list
    # if it is not a list type string
    except SyntaxError as e:
        return None


# Convert accessibility to float
def stringToFloat(string):
    try:
        return float(string)
    except Exception:
        return None


# Swap T to U and vise versa if needed
def swapBase(sequence, toSwap="T"):
    toSwap = toSwap.upper()
    if toSwap == "T":
        return sequence.replace("U", "T")
    elif toSwap == "U":
        return sequence.replace("T", "U")
    else:
        return "Invalid toSwap: Use T or U"

# CSV reading functions
# CSV Read for supp TABLE
# Want to make this into a dictionary
# returns a dictionary, Example:
# {65: {'length': 90, 'sRNA': 'ryhB', 'ranges': [[43,68], [9,50]]}}


def readSuppCSV(infile):
    # initialize dictionary
    reference_dict = dict()
    # bring in CSV file and read
    with open(infile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Skip Header
        readCSV.__next__()
        for row in readCSV:
            # set up wanted columns
            moleculeNum, sRNA, length, interacting, mRNA = row[0], row[1], row[3], row[15], row[14]
            # exclude those that do not have interacting nucleotides
            # by checking if the cell is empty
            if not interacting.strip():
                continue
            # set the mRNA make, if it is not known make it not listed.
            if not mRNA.strip() or mRNA == "??":
                mRNA = "Not listed"
            try:
                # print("Molecule Num: {} sRNA: {} mRNA: {}".format(moleculeNum, sRNA, mRNA))
                length = int(length)
                interacting = stringToList(interacting)
                add_mRNA = (mRNA, interacting)
                # print(add_mRNA)
                addToDict(int(moleculeNum), reference_dict, interacting, sRNA, length, add_mRNA)
            except ValueError:
                interacting = stringToList(interacting)
                add_mRNA = (mRNA, interacting)
                addToDict(int(moleculeNum), reference_dict,
                          interacting, sRNA=sRNA, mRNA_map=add_mRNA)
    return reference_dict


def readSuppCSVRAW(infile):
    # initialize dictionary
    reference_dict = dict()
    # bring in CSV file and read
    with open(infile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Skip Header
        readCSV.__next__()
        for row in readCSV:
            # set up wanted columns
            moleculeNum, sRNA, length, interacting, = row[0], row[1], row[3], row[15]
            if not moleculeNum.strip():
                continue
            try:
                length = int(length)
                interacting = stringToList(interacting)
                addToDict(int(moleculeNum), reference_dict, interacting, sRNA, length)
            except ValueError:
                interacting = stringToList(interacting)
                addToDict(int(moleculeNum), reference_dict, interacting, sRNA=sRNA, )
    return reference_dict


def readSuppCSV_RNA(infile):
    # initialize dictionary
    reference_dict = dict()
    # bring in CSV file and read
    with open(infile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Skip Header
        readCSV.__next__()
        for row in readCSV:
            # set up wanted columns
            moleculeNum, sRNA, sequence = row[0], row[1], row[2]
            if not moleculeNum.strip():
                continue
            try:
                addToRNADict(int(moleculeNum), reference_dict, sRNA, swapBase(sequence, "U"))
            except ValueError:

                addToRNADict(int(moleculeNum), reference_dict, sRNA, swapBase(sequence, "U"))
    return reference_dict


def readHeatMap(infile):
    # Yield results so you can perform operations else where
    with open(infile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Skip header
        readCSV.__next__()
        for row in readCSV:
            # set up wanted columns
            moleculeNum, access, start, end = row[3], row[2], row[4], row[5]
            interacting = "[{},{}]".format(start, end)
            interacting = stringToList(interacting)
            access = stringToFloat(access)
            # skip those that have no interacting sites or acces is NaN
            if interacting is None or isnan(access):
                continue
            if len(interacting) > 1:
                raise Exception("Interacting is too long")
            # interacting[0] returns list of [start, end]
            yield int(moleculeNum), access, interacting[0]


# mapping comparisions
# INPUT: ranges: [Rx,Ry], ref_ranges [[start,stop],[start,stop],[start,stop]]
# compare start and stop, if it meets criteria, exit
def isInRange(ranges, ref_ranges):
    Rx, Ry = ranges[0], ranges[1]
    for subRange in ref_ranges:
        if Rx >= subRange[0] and Ry <= subRange[1]:
            return True
    return False


# check if any of the ranges is exact with an mRNA
def isExact(ranges, ref_ranges):
    # print("input", ranges, ref_ranges, end=" ")
    # check witch mRNA it is mapped to.
    Rx, Ry = ranges[0], ranges[1]
    return_string = ''
    # print("{} in {}".format(ranges, ref_ranges))
    for values in ref_ranges:
        # print("values", values)
        mRNA, subrange = values[0], values[1]
        if len(subrange) == 1:
            # check to see if the ranges are exact/or contained
            if Rx == subrange[0][0] and Ry == subrange[0][1]:
                # print("ranges being compared {},{} == {},{}".format(
                #    Rx, Ry, subrange[0][0], subrange[0][1]))
                return_string += "{}-EXACT;".format(mRNA)
            else:
                if isInRange(ranges, [subrange[0]]):
                    return_string += "{};".format(mRNA)
        else:
            print(mRNA, subrange)
            for value in subrange:
                if Rx == value[0] and Ry == value[1]:
                    return_string += "{}-EXACT;".format(mRNA)
                else:
                    if isInRange(ranges, [value]):
                        return_string += "{};".format(mRNA)
    return return_string


def isInPercent(ranges, ref_ranges, percent=.8):
    Rx, Ry = ranges[0], ranges[1]
    rangesList = list(range(Rx, Ry + 1))
    total = len(rangesList)
    for subRange in ref_ranges:
        Ref_x, Ref_y = subRange[0], subRange[1]
        subRangeList = list(range(Ref_x, Ref_y + 1))
        # count the number of values in the ranges list that is in the
        # sub ranges list
        num_in_ref = 0
        for val in rangesList:
            if val in subRangeList:
                num_in_ref += 1

        if (num_in_ref / total) >= percent:

            return True

    return False


def getLocation(ranges, length):
    a, b = ranges[0], ranges[1]
    midPoint = (a + b) / 2
    position = midPoint / length
    return position


def plotData(data1, data2, figure_name):

    plt.scatter(*zip(*data1), label="100{} contained within binding region".format("%"))
    plt.scatter(*zip(*data2), label="Not contained".format("%"), color='r')
    plt.xlabel("Position")
    plt.ylabel("Accessibility")
    plt.ylim([0, 1])
    plt.xlim([0, 1])
    fontP = FontProperties()
    fontP.set_size('small')
    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
    plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
    plt.savefig("{}.png".format(figure_name), dpi=300, bbox_inches="tight")


def listToStr(values):
    string = ''
    for value in values:
        string += str(value) + ","
    return string


def createCSV(outfile, data, header):
    with open("{}.csv".format(outfile), 'w') as csv_file:
        # Write Header
        csv_file.write(header)
        for line in data:
            if isinstance(line, list):
                line = listToStr(line)
            csv_file.write(line)
            csv_file.write('\n')


def createAllCSV(outfile, data):
    with open("{}.csv".format(outfile), 'w') as csv_file:
        # Write Header
        header = "molecule number,sRNA, accessibility, interacting site, \
        is 80 percent within binding region, supplementary table interacting nucleotides\n"
        csv_file.write(header)
        for line in data:
            csv_file.write(line)
            csv_file.write('\n')


def countBindingRegions(ref_dict):
    num_regions = 0
    for i in ref_dict:
        regions = len(ref_dict[i]["ranges"])
        num_regions += regions
    return num_regions


if __name__ == '__main__':
    pass
    # ref_dict = readSuppCSV("./csv_files/supp_table_new.csv")
    # toPickle(ref_dict, "supp_table_with_mRNA")
