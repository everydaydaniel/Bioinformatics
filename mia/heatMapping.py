import csv
import re
import pickle
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from math import isnan


# TODO: Remember to modularize this script
# TODO: Plot the data
# NOTE: You can yeild row results and preform operations on them
# NOTE: To import from a different script, from <script> (no ext) import * or function
# NOTE: Reference dict is a dict of dicts.


# Serialization functions
def toPickle(dictionary):
    with open("SupplementaryDict.pickle", 'wb') as handle:
        pickle.dump(dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)
        handle.close()


def getPickle(infile):
    with open(infile, 'rb') as handle:
        return pickle.load(handle)


# Dictionary functions
def addToDict(key, aDict, ranges, sRNA=None, length=None):
    # values are contained in a list to be able to add
    # multiple values to each key
    # store the length as a primary value since it would be redundandant
    # to store it for each key molecule
    if key not in aDict:
        if not isinstance(length, int):
            raise Exception("Length is not an int.")
        aDict[key] = {"length": length, "sRNA": sRNA, "ranges": [i for i in ranges]}
    else:
        # ERror check sRNA
        if aDict[key]['sRNA'] != sRNA:
            print(aDict[key]['sRNA'], sRNA)
            raise Exception("sRNA is different")
        for i in ranges:
            aDict[key]["ranges"].append(i)


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
    except Exception as e:
        return None


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
            moleculeNum, sRNA, length, interacting, = row[0], row[1], row[3], row[15]
            # exclude those that do not have interacting nucleotides
            # by checking if the cell is empty
            if not interacting.strip():
                continue
            try:
                length = int(length)
                interacting = stringToList(interacting)
                addToDict(int(moleculeNum), reference_dict, interacting, sRNA, length)
            except ValueError:
                interacting = stringToList(interacting)
                addToDict(int(moleculeNum), reference_dict, interacting, sRNA=sRNA, )
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


def getLoaction(ranges, length):
    a, b = ranges[0], ranges[1]
    midPoint = (a + b) / 2
    position = midPoint / length
    return position


def plotData(data1, data2):

    plt.scatter(*zip(*data1), label="Accessible")
    #plt.scatter(*zip(*data2), label="Not Accessible", color='r')
    plt.xlabel("Position")
    plt.ylabel("Accessibility")
    plt.title("Accessible")
    plt.ylim([0, 1])
    plt.xlim([0, 1])
    # plt.legend()
    plt.gca().xaxis.set_major_locator(MaxNLocator(prune='lower'))
    plt.savefig("figure_1.png", dpi=300)


def createCSV(outfile, data):
    with open("{}.csv".format(outfile), 'w') as csv_file:
        # Write Header
        header = "molecule number,sRNA, accessibility, interacting site, \
        supplementary table interacting nucleotides\n"
        csv_file.write(header)
        for line in data:
            csv_file.write(line)
            csv_file.write('\n')


def main():

    # # Pickling
    raw_dict = readSuppCSVRAW("supp_table_new.csv")
    # toPickle(new_dict)
    isAccesable = []
    notAccesable = []
    accessCSV = []
    noAccessCSV = []
    ref_dict = getPickle('SupplementaryDict.pickle')
    heat = readHeatMap("google_heat_map.csv")
    accesCount, notAccesCount = 0, 0
    for i in heat:
        num, access, interacting = i[0], i[1], i[2]

        if not checkDictKey(num, ref_dict):
            notAccesCount += 1
            position = getLoaction(interacting, raw_dict[num]["length"])
            notAccesable.append((position, access))
            # Molecule number, accesisbility, interacting, supp table interacting sites
            noAccessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
            continue
        if isInRange(interacting, ref_dict[num]["ranges"]):
            accesCount += 1
            length = ref_dict[num]["length"]
            position = getLoaction(interacting, length)
            isAccesable.append((position, access))
            # Molecule number, accesisbility, interacting, supp table interacting sites
            accessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
        else:
            notAccesCount += 1
            # Molecule number, accesisbility, interacting, supp table interacting sites
            noAccessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
    # print("accesable: {}  not Accesable: {}".format(accesCount, notAccesCount))
#    print(notAccesable)
    #plotData(isAccesable, notAccesable)
    createCSV("accesisbility_data", accessCSV)
    createCSV("no_accesibility_data", noAccessCSV)
    print(accesCount, notAccesCount)

if __name__ == '__main__':
    main()
