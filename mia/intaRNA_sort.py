import os
import csv
from heatMapping import *
from operator import itemgetter



def readFiles(fname):

    # create a list of dictionaies and then sort it
    list_of_dictionaries = []
    id_num = 0
    with open(fname,"r") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        # skip header
        readCSV.__next__()
        for row in readCSV:
            dict_to_append = {}
            dict_to_append["row"] = row
            dict_to_append["energy"] = eval(row[8])
            list_of_dictionaries.append(dict_to_append)
    # sort the list
    sortedList = sorted(list_of_dictionaries, key=itemgetter("energy"))

    # cut the list to the first 100
    sortedList = sortedList[:100]
    list_to_return = [dictionary["row"] for dictionary in sortedList]



    return list_to_return



def main():

    path_to_results = "/Users/Thomas/Desktop/daniel/Bioinformatics-dev-branch/mia/inta_rna_results_raw_no_overlap"
    # change directory
    os.chdir(path_to_results)

    for fname in os.listdir("."):
        current_dir = os.getcwd()
        data = readFiles(fname)
        name = os.path.splitext(fname)[0]
        header = "id1,start1,end1,id2,start2,end2,subseqDP,hybridDP,E,current range,matched range,position,accessibility\n"
        os.chdir("../new_inta_rna_raw_no_overlap")
        createCSV("{}_top_100_raw".format(name),data,header)
        print("{}:".format(name.split("_")[0]),"100th no overlap value:",data[-1][8])
        os.chdir(current_dir)

if __name__ == '__main__':
    main()
