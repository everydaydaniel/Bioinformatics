import csv
import matplotlib.pyplot as plt

'''
This script will take in data from matrix creator and create a histogram
based on the input you want
'''


# get the row or rows that you want to create a histogram with given gene names.
# input: path/to/filename [list,of,gene,names].
def getRows(filename, geneNames):
    # csv file is in this format: genename, 1, 2, 3.......
    # intialize rows
    rows = {}

    with open(filename, "r") as csvFile:
        histogramReader = csv.reader(csvFile)
        # skip header
        histogramReader.__next__()
        for row in histogramReader:
            if row[0] in geneNames:
                rows[row[0]] = list(map(int, row[1:]))
            # this means we have found all the rows we want to make histograms out of
            # and dont need to continue looping
            if len(rows) == len(geneNames):
                break
    return rows


def plotData(data):
    print(data)
    x_len = [i for i in range(1, len(data) + 1)]
    print(max(data))
    plt.hist(x=x_len, weights=data, bins=len(data), histtype="step")
    plt.ylabel("Frequency")
    plt.xlabel("Posisiton")
    plt.show()


# split input names into rows for the get rows function.
# dont need this until later


def splitNames(names):
    pass


def main():
    geneNames = ["RyeF-35"]
    rows = getRows("./testFiles/histogramTest/processed.Sample.12.csv", geneNames)
    data = rows["RyeF-35"]
    plotData(data)

if __name__ == '__main__':
    main()
