import csv


# take in an outfile name a list of data where each entry is a
# prepared string and a header. delimiter option is for later
def write_csv(outfile, data, header, delimiter=","):
    with open("{}.csv".format(outfile), 'w') as csvfile:
        header += "\n"
        csvfile.write(header)
        for line in data:
            line += "\n"
            csvfile.write(line)
