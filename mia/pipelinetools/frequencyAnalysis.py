import argparse
import csv
import os
import re
import numpy as np


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "path", help="Input the path to a folder containing your samples. Samples must be in a folder to run this script.")
    parser.add_argument("reference", help="Path to reference genome.")

    parser.add_argument("-o", "--output", type=str,
                        help="Set the output filename, default will be frequecyAnalysis.csv")

    return parser.parse_args()


def weighted_std_dev(frequencies, positions, WA):
    # frequencies = [array], positions = [array], WA = Constant
    denominator = sum(frequencies) - 1
    if denominator == 0:
        return "nan"
    sum_numerator = 0
    for i in range(len(frequencies)):
        sum_numerator += (frequencies[i] * (positions[i] - WA)**2)
    denominator = sum(frequencies) - 1

    return np.sqrt(sum_numerator / denominator)

# get path to files
# input: directory/path
# output: ["path", "to","files", "in", "directory"]


def sorted_aphanumeric(data):
    convert = lambda text: int(text) if text.isdigit() else text.lower()
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(data, key=alphanum_key)


def getFilePaths(directory):
    paths = []
    for fname in sorted_aphanumeric(os.listdir(directory)):
        paths.append(directory + "{}".format(fname))
    return paths


def checkFilePaths(directory):
    # use this to check if all the files exist to begin with. If they
    # dont the raise the error staing wich path doesnt exist. This will save the
    # user time.
    pass


class AnalyzeFiles(object):

    def __init__(self, paths=[], outputName=None, reference_genome=None):  # None for testing only
        self.paths = paths
        self.outputName = outputName
        self.reference_genome = reference_genome
        self.read_data = []  # this will be used to hold all the data
        self.log_data = {}
        self.sampleNumbers = []
        self.sRNAGroups = {}
        self.min_max = {}
        self.normailized_adj_WA = {}  # dictionary to hold all normilized adj weighterd averages
        self.geneNames = None

    # this retrieves the sample numbers
    def retrieve_sample_numbers(self):
        for fname in self.paths:
            sample = "".join([i for i in fname if i.isdigit()])
            self.sampleNumbers.append(sample)
        if len(self.sampleNumbers) < len(self.paths):
            for i in range(len(self.sampleNumbers) + 1, len(self.paths) + 1):
                self.sampleNumbers.append(i)

    # Want to set a dictionary with values as such. Why? need these values to
    # for compute averages fo error propogation.
    # access => dict[sample][gene]["normalized_WA"]
    # we are going ot use this to gather information for later statisitics
    def set_normalized_WA(self, merged):
        for gene in merged:
            for sample in merged[gene]:
                adj_WA = merged[gene][sample]['adj_weighted_average']
                _min, _max = self.get_min_max(gene, sample, merged)
                norm_wa = None
                if adj_WA == "N/A":
                    norm_wa = "N/A"
                if _min == None or _max == None:
                    norm_wa = "N/A"
                if norm_wa != "N/A":
                    norm_wa = (adj_WA - _min) / (_max - _min)
                if sample not in self.normailized_adj_WA:
                    self.normailized_adj_WA[sample] = {}
                if gene not in self.normailized_adj_WA[sample]:
                    self.normailized_adj_WA[sample][gene] = {'normalized_WA': norm_wa}

    def error_propigation(self):
        pass

    # we clculate the normilized weighted average for use in the CSV
    def normalized_adj_WA(self, adj_WA, gene, sample, merged):
        _min, _max = self.get_min_max(gene, sample, merged)
        if adj_WA == "N/A":
            return "N/A"
        if _min == None or _max == None:
            return "N/A"
        return (adj_WA - _min) / (_max - _min)

    # set the min max for a group of sRNA
    # desired structure: min_max[sample][gene] = {min: val, max: val}
    def set_min_max(self, gene, sample, merged):
        values = []
        for sRNA in self.sRNAGroups[gene]:
            values.append(merged[sRNA][sample]['adj_weighted_average'])
        # sift out non numbers
        values = [i for i in values if not isinstance(i, str)]
        if len(values) < 2:
            self.min_max[sample][gene] = {"min": None, "max": None}
        else:
            self.min_max[sample][gene] = {"min": min(values), "max": max(values)}

    # retrieve the min and max of a given sample
    # input: dataset[gene][sample_number]
    # output: min_max[sample][gene][min] and min_max[gene][sample][max]
    def get_min_max(self, gene, sample_number, merged):
        gene = gene.split("-")[0]

        if sample_number not in self.min_max:
            self.min_max[sample_number] = {}
        if gene not in self.min_max[sample_number]:  # only need to do this once per sRNA
            self.set_min_max(gene, sample_number, merged)
            # after this step that dictionart Key value pair will exist
        return (self.min_max[sample_number][gene]["min"], self.min_max[sample_number][gene]["max"])

    # This method will get all the sRNA groups for normalization purposes
    # Example:
    # input = reference_genome order
    # output = {'tpke': ['tpke-1','tpke-2'...]}
    # this will run within genome parse so that it can be done after getting the order
    def get_srna_groups(self, order):
        for value in order:
            base_sRNA = value.split("-")[0]
            if base_sRNA not in self.sRNAGroups:
                self.sRNAGroups[base_sRNA] = [value]
            else:
                self.sRNAGroups[base_sRNA].append(value)

    # This method will grab all the genomes from the reference genome and
    # put all the names in a list. The reason for this is so we can call
    # all the data dictionary in a "sorted" order.
    def geneome_parse(self):
        genome_order = []
        if os.path.exists(self.reference_genome):
            with open(self.reference_genome, "r") as reference:
                for row in reference:
                    if row[0] == ">":
                        genome_order.append(row[1:].strip())
        else:
            raise FileNotFoundError(
                "{} file does not exist. Check path to file.".format(self.reference_genome))
        self.get_srna_groups(genome_order)
        return genome_order

    def readCSV(self, path):
        # for indovidual file reading
        with open(path, 'r') as csvfile:
            csvRead = csv.reader(csvfile, delimiter=",")
            # skip header
            csvRead.__next__()
            for row in csvRead:
                yield row

    def analysis(self, path):
        reader = self.readCSV(path)
        length = 0
        data = {}
        data["fileName"] = path.split("/")[-1]
        for row in reader:
            name = row[0]
            # frequencies in the data
            frequencies = list(map(float, row[1:]))
            # only need to do this once
            if length == 0:
                length = len(frequencies)
                data["length"] = length
            positions = list(range(1, length + 1))
            # get the weighted avereage, standard deviation and sum of all the reads
            weighted_average = np.average(positions, weights=frequencies)
            std_dev = weighted_std_dev(frequencies, positions, weighted_average)
            num_reads = sum(frequencies)
            adj_weighted_average = weighted_average - 164
            if adj_weighted_average < 0:
                adj_weighted_average = "N/A"
            # insert the read name as a key that contains a dictionary
            # of the statistics
            # example to access will be data[readName][statisticName]
            data[name] = {
                "weighted_average": weighted_average,
                "std_dev": std_dev,
                "num_reads": num_reads,
                "adj_weighted_average": adj_weighted_average,
            }
        # append the data from one file into the read data list
        self.read_data.append(data)

    def merge(self):
        # We will execute all the methods here to produce our data
        # first collect all the data from all reads
        for fname in self.paths:
            # collects all the data from the csv sheets
            print("Analyzing sample {}".format(fname))
            self.analysis(fname)
        print("Merging data.")
        # by now the self.read_data list should be populated
        merged = {}  # ideally I should've merged in the analysis step because now we are taking up more memory
        # will probably fix later
        # gene "sorted" name

        geneNames = self.geneNames  # list of genes from reference genome
        for sampleNumber, sampleData in enumerate(self.read_data):
            currentSample = sampleNumber + 1
            # What we want to do here is combine all the file statistics so we can write it into
            # a csv. we want the merged dict to look like the following
            # merged[geneName] : [1:{"WA" 10, "num reads" : 20 etc.},
            # 2:{"WA" 10, "num reads" : 20 etc.}]
            for gene in geneNames:
                if gene in sampleData:
                    if gene not in merged:
                        merged[gene] = {}  # initialize an index for gene
                    merged[gene][currentSample] = sampleData[gene]
                else:
                    if gene not in merged:
                        merged[gene] = {}  # initialize an index for gene
                    merged[gene][currentSample] = {
                        'num_reads': "N/A",
                        'std_dev': "N/A",
                        'weighted_average': "N/A",
                        'adj_weighted_average': "N/A",
                    }
        # set the min max dictionary

        # return the merged ditionary and the number of samples analyzed
        return merged, [i for i in range(1, currentSample + 1)], geneNames

    def main(self):
        # want to write all the merged files into a csv file
        self.geneNames = self.geneome_parse()
        merged, order, genes = self.merge()
        self.set_normalized_WA(merged)
        analysis_cols = ["W/A", "Std dev", "Num reads", "Adj W/A", "Norm adj W/A"]
        num_samples = len(order)
        with open("{}.csv".format(self.outputName), "w") as csvFile:
            header = "gene,"
            for count, col in enumerate(self.sampleNumbers):
                header += ",".join(["sample{} {}".format(col, i) for i in analysis_cols])
                header += ","
            # print(header)
            header = header[:-1]
            header += "\n"
            csvFile.write(header)
            for gene in genes:
                toWrite = "{}".format(gene)

                for sample in order:
                    # if the number of reads is less than 3 then we dont consider it
                    if merged[gene][sample]["num_reads"] == "N/A" or merged[gene][sample]["num_reads"] < 3:
                        toWrite += ",{},{},{},{},{}".format(
                            "not enough reads", "not enough reads", "not enough reads", "not enough reads", "not enough reads")
                    else:
                        weighted_average = merged[gene][sample]["weighted_average"]
                        standard_deviation = merged[gene][sample]["std_dev"]
                        num_reads = merged[gene][sample]["num_reads"]
                        adj_weighted_average = merged[gene][sample]["adj_weighted_average"]
                        normalized_WA = self.normailized_adj_WA[sample][gene]['normalized_WA']
                        # normalized_WA = self.normalized_adj_WA(
                        #     adj_weighted_average, gene, sample, merged)
                        toWrite += ",{},{},{},{},{}".format(weighted_average, standard_deviation,
                                                            num_reads, adj_weighted_average, normalized_WA)
                toWrite += "\n"
                csvFile.write(toWrite)


def main():
    args = parseArguments()

    path, output, reference = args.path, args.output, args.reference
    if output == None:
        output = "frequecyAnalysis"

    # analyze = AnalyzeFiles(reference_genome="INTERFACE_genome.fa")
    # read = analyze.analysis("samples/frequencies_analysis_sample.csv")
    # parse = analyze.geneome_parse()
    paths = getFilePaths(path)

    print("Analyzing files in {}\nReference genome file is: {}\nResults will be output to {}.csv.".format(
        path, reference, output))
    # paths = getFilePaths("samples/recentResults")
    analyze = AnalyzeFiles(paths, output, reference)
    analyze.retrieve_sample_numbers()
    analyze.main()
    print("Done.")

if __name__ == '__main__':
    main()
