import os
import csv
from heatMapping import *


# global count to see how many sequences are mapped to the hotspots
count = 0


# read in the hotspots csv file and map acordingly
def readHotSpotsCSV(infile, ref_dict):
    hotspot_dict = {}
    with open(infile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        readCSV.__next__()
        for row in readCSV:
            # row[4] contains the * that means we keep it
            if row[4].strip():
                key, position, accessibility, interacting = row[0], row[1], row[2], row[3]
                key, position, accessibility, interacting = int(key), eval(
                    position), eval(accessibility), eval(interacting.replace("-", ","))

                # swap the keys
                sRNA = ref_dict[key]["sRNA"]
                # populate the dictionary yo!
                # dict is "sRNA": "ranges" {[(position,accessibility,interacting)]}
                if sRNA in hotspot_dict:
                    values = (position, accessibility, interacting)
                    hotspot_dict[sRNA]["ranges"].append(values)
                else:
                    values = (position, accessibility, interacting)
                    hotspot_dict[sRNA] = {"key": key, "ranges": [values]}
        return hotspot_dict


# read the csv
# return the row if it passes the overlap criteria
# input (inflile name, key name= sRNA, ref_dict = dicionary)
def csv_read(infile, key_name, ref_dict, overlap=5):
    # print("infile: {} key_name: {}".format(infile, key_name))
    ranges = ref_dict[key_name]["ranges"]
    # print(ranges)
    data = []
    with open(infile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=";")
        # skip header
        readCSV.__next__()

        for row in readCSV:
            values = overlap_analysis(row, ranges, overlap)
            if values:
                if values[1] not in ref_dict[key_name]["ranges"]:
                    # print("{} not in {}".format(values, ref_dict[key_name]["ranges"]))
                    break
                position, accessibility = values[1][0], values[1][1]
                matched_range = "[{}-{}]".format(values[1][-1][0], values[1][-1][1])
                range_in_row = "[{}-{}]".format(row[4], row[5])
                # print("{} is in {} with position {} and accessibility {}".format(
                # range_in_row, matched_range, position, accessibility))
                # range_in_row = the start and end points
                # matched_range = the hotspot overlap
                # position and accessibility are the same
                to_add = [range_in_row, matched_range, position, accessibility]
                row += to_add
                # print(row)
                data.append(row)
                globals()["count"] += 1
        if len(data) == 0:
            data.append("No hotspot matches found")
        return data


# check the refernce ranges, if they overlap then keep else TOSS it.
def overlap_analysis(row, ranges, overlap):
    start, end = int(row[4]), int(row[5])
    current_range = list(range(start, end + 1))

    for subrange in ranges:
        subRangeList = list(range(subrange[-1][0], subrange[-1][1] + 1))
        count = 0
        for value in current_range:
            if value in subRangeList:
                count += 1
            if count >= overlap:
                # print("\n\nTRUE\nstart: {} end: {}\ncurrent range :{}\nmatched subrange:
                # {}\nrange list: {}".format(
                    # start, end, current_range, subRangeList, ranges))
                return True, subrange, current_range
    return False


def getName(nameList):
    name = ''
    for i in range(len(nameList)):
        name += nameList[i]
        if nameList[i + 1] == "IntaRNA":
            break
        # this is very specific and general
        if nameList[i + 1] == "42":
            name += "_"
    return name


def reverseKeys(dictionary1, dictionary2):
    new_dict = {}

    for key in dictionary2:
        new_dict[dictionary1[key]["sRNA"]] = dictionary1[key]
        new_key = dictionary1[key]["sRNA"]
        new_dict[new_key]["sequence"] = dictionary2[key]["sequence"]
        new_dict[new_key]["key"] = key
    return new_dict


# if the key is in the dictionary return true, else false
def check_key(key, dictionary):
    try:
        dictionary[key]
        return True

    except KeyError as e:
        print("{} not in hotspot dict".format(key))
        return False


# list dir is giving us .ds store
def isHiddenFile(fname, ext):
    if fname.startswith("."):
        return True
    if ext != ".csv":
        return True
    else:
        return False


def main():
    # initialize
    interacting_dict = getPickle("./sRNA_with_interacting_nucleotides.pickle")
    supplementary_table = getPickle("./SupplementaryDict.pickle")
    reversed_dict = reverseKeys(supplementary_table, interacting_dict)
    path_to_dir = "{}/IntaRNA_results".format(os.getcwd())
    hotspot_dict = readHotSpotsCSV(
        "./csv_files/not_100_percent_contained_specs_included.csv", interacting_dict)

    os.chdir(path_to_dir)

    for fname in os.listdir("."):
        name, ext = os.path.splitext(fname)
        if isHiddenFile(fname, ext):
            continue
        key_name = getName(name.split("_"))
        if not check_key(key_name, hotspot_dict):
            continue
        data = csv_read(fname, key_name, hotspot_dict, overlap=5)
        filename = "{}_hotspot_analysis".format(name)
        header = "id1,start1,end1,id2,start2,end2,subseqDP,hybridDP,E,current range,matched range,position,accessibility\n"
        current_dir = os.getcwd()
        os.chdir("../inta_rna_results")
        createCSV("{}".format(filename), data, header)
        os.chdir(current_dir)
    print(count)

if __name__ == '__main__':
    main()
