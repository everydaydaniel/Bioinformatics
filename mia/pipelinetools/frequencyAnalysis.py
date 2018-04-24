import csv
import os
import re
import numpy as np

# TODO: make the interface for command line


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
        paths.append(directory + "/{}".format(fname))
    return paths


def checkFilePaths(directory):
    # use this to check if all the files exist to begin with. If they
    # dont the raise the error staing wich path doesnt exist. This will save the
    # user time.
    pass


class AnalyzeFiles(object):

    def __init__(self, paths=[], reference_genome=None):  # None for testing only
        self.paths = paths
        self.dictionaries = [{} for i in range(len(self.paths))]
        self.reference_genome = reference_genome
        self.read_data = []  # this will be used to hold all the data
        self.log_data = {}
        self.sampleNumbers = []
        self.sRNAGroups = {}

    # this retrieves the sample numbers
    def retrieve_sample_numbers(self):
        for fname in self.paths:
            sample = "".join([i for i in fname if i.isdigit()])
            self.sampleNumbers.append(sample)
        if len(self.sampleNumbers) < len(self.paths):
            for i in range(len(self.sampleNumbers) + 1, len(self.paths) + 1):
                self.sampleNumbers.append(i)

    # This method will get all the sRNA groups for normalization purposes
    # Example:
    # input = reference_genome
    # output = {'tpke': ['tpke-1','tpke-2'...]}
    # this will run witin genome parse so that it can be done after getting the order
    def get_srna_groups(order):
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
        get_srna_groups(genome_order)
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
            # insert the read name as a key that contains a dictionary
            # of the statistics
            # example to access will be data[readName][statisticName]
            data[name] = {
                "weighted_average": weighted_average,
                "std_dev": std_dev,
                "num_reads": num_reads,
            }
        # append the data from one file into the read data list
        self.read_data.append(data)

    def merge(self):
        # We will execute all the methods here to produce our data
        # first collect all the data from all reads
        for fname in self.paths:
            # collects all the data from the csv sheets
            self.analysis(fname)
        # by now the self.read_data list should be populated
        merged = {}  # ideally I should've merged in the analysis step because now we are taking up more memory
        # will probably fix later
        # gene "sorted" name
        geneNames = self.geneome_parse()  # list of genes from reference genome
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
                        'weighted_average': "N/A"
                    }
        # return the merged ditionary and the number of samples analyzed
        return merged, [i for i in range(1, currentSample + 1)], geneNames

    def main(self):
        # want to write all the merged files into a csv file
        merged, order, genes = self.merge()
        analysis_cols = ["W/A", "Std dev", "Num reads"]
        num_samples = len(order)
        with open("output.csv", "w") as csvFile:
            header = "gene,"
            for count, col in enumerate(self.sampleNumbers):
                header += ",".join(["sample{} {}".format(col, i) for i in analysis_cols])

                header += ","
            print(header)
            header = header[:-1]
            header += "\n"
            csvFile.write(header)
            for gene in genes:
                toWrite = "{}".format(gene)
                for sample in order:
                    weighted_average = merged[gene][sample]["weighted_average"]
                    standard_deviation = merged[gene][sample]["std_dev"]
                    num_reads = merged[gene][sample]["num_reads"]
                    toWrite += ",{},{},{}".format(weighted_average, standard_deviation, num_reads)
                toWrite += "\n"
                csvFile.write(toWrite)


def main():
    # analyze = AnalyzeFiles(reference_genome="INTERFACE_genome.fa")
    # read = analyze.analysis("samples/frequencies_analysis_sample.csv")
    # parse = analyze.geneome_parse()
    paths = getFilePaths("samples/recentResults")
    print(paths)
    analyze = AnalyzeFiles(paths, "INTERFACE_genome.fa")
    analyze.retrieve_sample_numbers()
    analyze.main()

if __name__ == '__main__':
    main()
