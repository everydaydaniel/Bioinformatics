import csv
import re

# NOTES
# If it has a blank interacting nucleotides column the don't
# include!!!!


def addToDict(molecule, access, accessRange, aDict):
    if molecule not in aDict:
        aDict[molecule] = (access, accessRange)
    else:
        aDict[molecule].append((access, accessRange))


# READ IN CSV FILE FOR SUPPLEMENTARY TABLE
def readSuppCSV(infile):
    with open(infile, "r") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        # row parameters
        number, sRNA, targetmRna, interacting = 0, 1, 14, 15
        rowNum = 1
        for row in readCSV:
            if len(row[interacting].strip()) == 0:
                continue
            else:
                print(row[number], row[sRNA], row[targetmRna], row[interacting])

            rowNum += 1


# READ CSV OF HEAT MAP TABLE
def readHeatCSV(infile):
    with open(infile, 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # row parameters
        access, number, start, end = 2, 3, 4, 5
        molecule_dict = dict()
        count = 1
        for row in readCSV:
            if count == 1:
                count += 1
                continue
            # Clean data
            try:
                # To assign multiple values to a key, the values must be stored in a list.
                molecule, accessibility, accessRange = int(row[number]), float(row[access]), [
                    int(row[start]), int(row[end])]
                if not molecule in molecule_dict:
                    molecule_dict[molecule] = [(accessibility, accessRange)]
                else:
                    toAdd = (accessibility, accessRange)
                    molecule_dict[molecule].append(toAdd)
            # encounter an empty range, then skip
            except ValueError as e:
                continue

        return molecule_dict


def main():
    # Currently works
    # readSuppCSV("supplementary_table_no_merges.csv")
    molecule_dict = readHeatCSV("google_heat_map.csv")

    # MAIN
    contained = []
    not_contained = []
    with open("supp_table_new.csv", "r") as csvfile:
        readCSV = csv.reader(csvfile, delimiter=",")
        # row parameters
        number, sRNA, targetmRna, interacting = 0, 1, 14, 15
        rowNum = 1
        for row in readCSV:
            if rowNum == 1:
                rowNum += 1
                continue
            else:
                try:
                    # set parameters
                    molecule, sRna = int(row[number]), row[sRNA]
                    interactingNuc = row[interacting]
                    # Count number of commas,
                    # if none, then skip
                    # if theres one then == one list
                    # if more than one == multiple lists
                    if len(re.findall(r",", interactingNuc, re.IGNORECASE)) == 0:
                        continue
                    elif len(re.findall(r",", interactingNuc, re.IGNORECASE)) == 1:
                        interactingNuc = eval(row[interacting])
                    else:
                        # get matches, make psuedo list string, eval string in list comprehension
                        matches = re.findall(r"\[(.*?)\]", interactingNuc, re.IGNORECASE)
                        multiple_lists = []
                        for i in matches:
                            multiple_lists.append("[{}]".format(i))
                        interactingNuc = [eval(i) for i in multiple_lists]
                        interactingNuc = tuple(interactingNuc)

                    # START COMPARING TO HEAT MAP
                    heatMapVals = molecule_dict[molecule]
                    # print(interactingNuc)
                    for vals in heatMapVals:
                        Mx = vals[-1][0]
                        My = vals[-1][1]
                    # 	print(Mx,My)
                    # print("\n\n")
                        if isinstance(interactingNuc, list):
                            if interactingNuc[0] >= Mx and interactingNuc[1] <= My:
                                values = (molecule, sRna, interactingNuc)
                                contained.append(values)
                                break
                            # else:
                            # not_contained.append(values)
                        elif isinstance(interactingNuc, tuple):
                            for sub_list in interactingNuc:
                                if sub_list[0] >= Mx and sub_list[1] <= My:
                                    values = (molecule, sRna, interactingNuc)
                                    contained.append(values)
                                    break

                    values = (molecule, sRna, interactingNuc)
                    not_contained.append(values)

                except ValueError as e:
                    continue

    for i in contained:
        if i in not_contained:
            not_contained.remove(i)
    print(len(contained), len(not_contained))
    for i in contained:
        print(i)


if __name__ == '__main__':
    main()
