import subprocess
import sys
import os
import random
import pickle


# Get the minimum free energy value (mfe)
# it is the third line proceding a line
# with %%%%%%%%%%%%% signs
def getAfinityVal(f):
    with open(f, "r") as mfe:
        strand = os.path.splitext(f)[0]
        start = 0
        marker = "%%%%%%%%%%%%".format()
        for line in mfe:
            if marker in line:
                start += 1
            if start >= 1:
                if start == 3:
                    return strand, float(line.strip())
                start += 1
        # if the mfe didnt return a value
        # return zero.
        if start == 0:
            return strand, 0.0


# Go to the directory containing the *.mfe files
# and get the MFE values from each file
def generateDict(directory):
    currentDir = os.getcwd()
    os.chdir("./{}".format(directory))
    mfeDict = {}
    for f in os.listdir(os.getcwd()):
        # get strand and mfe vals
        strand, mfe = getAfinityVal(f)
        # add to the dictionary
        mfeDict[strand] = mfe
    os.chdir(currentDir)
    return mfeDict


# create a list of values with tuples
# pythion sorts lists with tuples based
# off of the first element in the tuple
def getMaxVals(mfeDict):
    max_vals = []

    for key in mfeDict:
        if len(max_vals) != 10:
            max_vals.append((mfeDict[key], key))
        else:
            # compare tuples to sort
            if (mfeDict[key], key) < max(max_vals):
                # get index of min value, pop it then apend new max value
                idx = max_vals.index(max(max_vals))
                max_vals.pop(idx)
                max_vals.append((mfeDict[key], key))
    return max_vals


def randomSample(mfeDict):
    randomInts = random.sample(range(len(mfeDict)), 10)
    randomList = []
    count = 0
    for i in mfeDict:
        if count in randomInts:
            randomList.append((mfeDict[i], i))
        count += 1
    return randomList


# Serialize the dict to a pickle file for later use.
def createPickledDict(mfeDict):
    with open("mfeDict.pickle", 'wb') as outfile:
        pickle.dump(mfeDict, outfile,  protocol=pickle.HIGHEST_PROTOCOL)


def createDict(pickleFile):
    with open(pickleFile, 'rb') as infile:
        return pickle.load(infile)


def main():
    # os.chdir("./analysis/nupackmfe")
    mfeDict = generateDict("./nupackmfe")
    max_values = getMaxVals(mfeDict)
    randomValues = randomSample(mfeDict)


if __name__ == '__main__':
    main()

else:
    # # # GLOBALS # # #
    # These variables will be available
    # when imported
    # This is newly discovered and its pretty awesome
    mfeDictionary = createDict("analysis/mfeDict.pickle")
