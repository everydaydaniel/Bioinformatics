from heatMapping import *
import os


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
            position = getLocation(interacting, raw_dict[num]["length"])
            notAccesable.append((position, access))
            # Molecule number, accessibility, interacting, supp table interacting sites
            noAccessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
            continue
        if isInRange(interacting, ref_dict[num]["ranges"]):
            accesCount += 1
            length = ref_dict[num]["length"]
            position = getLocation(interacting, length)
            isAccesable.append((position, access))
            # Molecule number, accessibility, interacting, supp table interacting sites
            accessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
        else:
            notAccesCount += 1
            # Molecule number, accessibility, interacting, supp table interacting sites
            notAccesable.append((position, access))
            noAccessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
    # print("accesable: {}  not Accesable: {}".format(accesCount, notAccesCount))
    # print(notAccesable)
    # plotData(isAccesable, notAccesable)
    # createCSV("accessibility_data", accessCSV)
    # createCSV("no_accesibility_data", noAccessCSV)
    print(accesCount, notAccesCount)


def newAnalysis():
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
            position = getLocation(interacting, raw_dict[num]["length"])
            notAccesable.append((position, access))
            # Molecule number, accessibility, interacting, supp table interacting sites
            noAccessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
            continue
        if isInRange(interacting, ref_dict[num]["ranges"]) or isInPercent(interacting, ref_dict[num]["ranges"]):
            accesCount += 1
            length = ref_dict[num]["length"]
            position = getLocation(interacting, length)
            isAccesable.append((position, access))
            # Molecule number, accessibility, interacting, supp table interacting sites
            accessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
        else:
            notAccesCount += 1
            # Molecule number, accessibility, interacting, supp table interacting sites
            noAccessCSV.append("{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(raw_dict[num]["ranges"]).replace(",", "-")))
    # print("accesable: {}  not Accesable: {}".format(accesCount, notAccesCount))
    # print(notAccesable)
    # plotData(isAccesable, notAccesable)
    # createCSV("accessibility_data_with_percent_threshold", accessCSV)
    # createCSV("no_accesibility_data_with_percent_threshold", noAccessCSV)
    print(accesCount, notAccesCount)
    print("Ref_dict: {} Raw_dict: {}".format(
        countBindingRegions(ref_dict), countBindingRegions(raw_dict)))


def allAccess():
    # # Pickling
    raw_dict = readSuppCSVRAW("csv_files/supp_table_new.csv")
    # toPickle(new_dict)
    isAccesable = []
    notAccesable = []
    accessCSV = []
    noAccessCSV = []
    allAccessCSV = []
    hundred_percent_contained = []
    hundred_percent_not_contained = []
    ref_dict = getPickle('SupplementaryDict.pickle')
    heat = readHeatMap("csv_files/google_heat_map.csv")
    accesCount, notAccesCount = 0, 0
    flag = 0
    for i in heat:
        num, access, interacting = i[0], i[1], i[2]

        if len(raw_dict[num]["ranges"]) == 0:
            continue
        if not checkDictKey(num, ref_dict):
            flag += 1
            notAccesCount += 1
            position = getLocation(interacting, raw_dict[num]["length"])
            notAccesable.append((position, access))
            hundred_percent_not_contained.append(
                "{},{},{}".format(raw_dict[num]["sRNA"], position, access))
            # Molecule number, accessibility, interacting, supp table interacting sites
            allAccessCSV.append("{},{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(0), str(raw_dict[num]["ranges"]).replace(",", "-")))
            continue
        if isInRange(interacting, ref_dict[num]["ranges"]):
            accesCount += 1
            length = ref_dict[num]["length"]
            position = getLocation(interacting, length)
            isAccesable.append((position, access))
            hundred_percent_contained.append("{},{},{}".format(
                raw_dict[num]["sRNA"], position, access))
            # Molecule number, accessibility, interacting, supp table interacting sites
            allAccessCSV.append("{},{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(1), str(raw_dict[num]["ranges"]).replace(",", "-")))
        else:
            notAccesCount += 1
            position = getLocation(interacting, raw_dict[num]["length"])
            notAccesable.append((position, access))
            hundred_percent_not_contained.append(
                "{},{},{},{}".format(num, position, access, str(interacting).replace(",", "-")))
            # Molecule number, accessibility, interacting, supp table interacting sites
            allAccessCSV.append("{},{},{},{},{},{}".format(
                num, raw_dict[num]["sRNA"], access, str(interacting).replace(",", "-"), str(0), str(raw_dict[num]["ranges"]).replace(",", "-")))
            # print("sRNA: {}, Num: {}, Position: {}, Access: {}, Interacting: {}".format(
            #     raw_dict[num]["sRNA"], num, position, access, str(interacting).replace(",", "-")))
    # print("accesable: {}  not Accesable: {}".format(accesCount, notAccesCount))
    # print(notAccesable)
    # plotData(isAccesable, notAccesable)
    # createCSV("accessibility_data_with_percent_threshold", accessCSV)
    # createCSV("no_accesibility_data_with_percent_threshold", noAccessCSV)
    # print(accesCount, notAccesCount)
    # print(len(isAccesable), len(notAccesable))
    # print("Ref_dict: {} Raw_dict: {}".format(
    #    countBindingRegions(ref_dict), countBindingRegions(raw_dict)))
    #  createAllCSV("Heatmap_has_binding_region", allAccessCSV)
    # plotData(isAccesable, notAccesable, "within_100_percent")
    header = "Molecule Number, Position, accessibility, Interacting Nucleotides\n"
    #createCSV("not_100_percent_contained", hundred_percent_not_contained, header)

    print("length isAccesable: {} length Not Accesable: {}\nlength 100 percent contained:{} length 100 percent not contained: {}".format(
        len(isAccesable), len(notAccesable), len(hundred_percent_contained), len(hundred_percent_not_contained)))
    for i in hundred_percent_not_contained:
        print(i)
    print('flag:{}'.format(flag))


def getNoInteracting():

    raw_dict = readSuppCSVRAW("csv_files/supp_table_new.csv")
    heat = readHeatMap("csv_files/google_heat_map.csv")
    ref_dict = getPickle('SupplementaryDict.pickle')
    throwAwayValues = []
    ref_dict_2 = getPickle("supplementary_reference_dictionary.pickle")

    for i in heat:
        num, access, interacting = i[0], i[1], i[2]

        if len(raw_dict[num]["ranges"]) == 0:
            position = getLocation(interacting, raw_dict[num]["length"])
            if position < 0.25:
                if access > .66 or access < .33:
                    # number, position, accessibility, interacting Nucleotides
                    lineToWrite = "{},{},{},{}".format(
                        num, position, access, str(interacting).replace(",", "-"))
    #                print(lineToWrite)
                    throwAwayValues.append(lineToWrite)
    # print(len(throwAwayValues))
    # header = "Molecule Number, Position, accessibility, Interacting Nucleotides\n"
    # createCSV("no_interacting_nucleotides_in_sRNA_and_within_constraints", throwAwayValues, header)


def testing():
    ref_dict = readSuppCSV_RNA("supp_table_new.csv")
    toPickle(ref_dict, "supplementary_reference_dictionary")


def getInteracting():
    raw_dict = readSuppCSVRAW("csv_files/supp_table_new.csv")
    ref_dict = getPickle('SupplementaryDict.pickle')
    ref_dict_2 = getPickle("supplementary_reference_dictionary.pickle")
    hasInteractingKeys = []
    for i in raw_dict:
        if len(raw_dict[i]['ranges']) != 0:
            print(raw_dict[i]['sRNA'], ref_dict[i]['sRNA'])
            hasInteractingKeys.append(i)
    print(len(hasInteractingKeys), len(ref_dict))
    hasInteractingNucleotidesDict = {}
    for key in hasInteractingKeys:
        hasInteractingNucleotidesDict[key] = ref_dict_2[key]
    print(hasInteractingNucleotidesDict)
    print(len(hasInteractingNucleotidesDict), len(hasInteractingKeys))
    toPickle(hasInteractingNucleotidesDict, "sRNA_with_interacting_nucleotides")

if __name__ == '__main__':
    getInteracting()
