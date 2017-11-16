import csv
import os


def listToString(values, delimiter=','):
    string = ''
    for value in values:
        string += str(value) + delimiter
    return string[:-1]


# take in an outfile name a list of data where each entry is a
# prepared string and a header. delimiter option is for later
def write_csv(outfile, data, header, delimiter=","):
    with open("{}.csv".format(outfile), 'w') as csvfile:
        header += "\n"
        csvfile.write(header)
        for line in data:
            line += "\n"
            csvfile.write(line)


# This csv writer will appened data to a csv
# data and header must be in list format.
# could re write to have an add header type.
def writeToCSV(outfile, data, header=[], delimiter=","):
    try:
        # make sure data is a list
        assert isinstance(data, list)
        assert isinstance(header, list)
        filename = "{}.csv".format(outfile)
        # if the file name exists we are appending to the file.
        if os.path.isfile(filename):
            with open(filename, 'a') as csvfile:
                writer = csv.writer(csvfile, delimiter=delimiter)
                writer.writerow(data)
        else:
            with open("{}.csv".format(outfile), 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter=delimiter)
                writer.writerow(header)
                writer.writerow(data)
    except AssertionError as e:
        print(e, 'data and header must be a list. ex ["hello", "world"]')


if __name__ == '__main__':
    header = ['this', 'is', 'a', 'test']
    data = [1, 2, 3, 4]
    writeToCSV("testWriteToCSV", data, header, delimiter=";")
    data = [5, 6, 7, 8]
    writeToCSV("testWriteToCSV", data)
    data = [1, 2, 3, "das,das,das,", 5, 6, [1, 2, 3, 4], 8]
    writeToCSV("testWriteToCSV", data, header, delimiter=";")


else:
    pass
