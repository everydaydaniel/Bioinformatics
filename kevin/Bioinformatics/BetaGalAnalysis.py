import csv
import os
from analysis.generateFASTA import *


# This script will run the sub sequences in TACC

def fold_sequence(target_dir, files_dir):
    try:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        current_dir = os.getcwd()
        path_to_target = current_dir + "/" + target_dir
        path_to_files = current_dir + "/" + files_dir + "/"

        for filename in os.listdir("./{}".format(files_dir)):
            name = os.path.splitext(filename)[0]
            os.chdir(path_to_target)
            print(os.getcwd())
            print("Fold {}{} {}_results.ct -mfe".format(path_to_files, filename, name))
            os.chdir(path_to_files)

    except Exception as e:
        raise


# create the files
# directory to put out files in, file containing sequences, prefix for filenames
def create_fasta(directory_name, filename, prefix=None):
    try:
        # create the directory if it does not exist
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        path_to_dir = os.getcwd() + "/" + directory_name + "/"
        current_dir = os.getcwd()

        with open("BetaGalPrep.csv", "r") as csvfile:
            readCSV = csv.reader(csvfile, delimiter=",")
            # skip header
            readCSV.__next__()
            for row in readCSV:
                sequences = row[4].split(";")
                position = row[0]
                codons = row[3].split(";")
                for i in range(len(sequences)):
                    sequence_name = "{}-{}".format(position, codons[i])
                    sequence_path = "{}{}".format(path_to_dir, sequence_name)
                    sequence = "{}".format(sequences[i])
                    generateFASTA(sequence_name, sequence, sequence_path)

    except Exception:
        raise


def main():
    # create_fasta("testDir", "BetaGalPrep.csv")
    fold_sequence("testResults", "testDir")

if __name__ == '__main__':
    main()
