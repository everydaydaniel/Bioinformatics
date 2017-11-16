from heatMapping import *
import os


# creates a fasta file with the given name and sequence.
def generateFASTA(sequenceName, sequence, sequence_path=None):

    # use sequence path so you dont have to do anoying change directory in code.
    if sequence_path is not None:
        with open("{}.fasta".format(sequence_path), 'w') as outfile:
            sequenceName, sequence = sequenceName.strip(), sequence.strip()
            toWrite = ">{}\n{}".format(sequenceName, sequence)
            outfile.write(toWrite)
    else:
        with open("{}.fasta".format(sequenceName), 'w') as outfile:
            sequenceName, sequence = sequenceName.strip(), sequence.strip()
            toWrite = ">{}\n{}".format(sequenceName, sequence)
            outfile.write(toWrite)


# def generateFASTA(sRNA, sequence, number):
#     with open("{}.fasta".format(sRNA), 'w') as outfile:
#         sRNA, sequence = sRNA.strip(), sequence.strip()
#         toWrite = ">{}-{}\n{}".format(number, sRNA, sequence)
#         print(toWrite)
#         outfile.write(toWrite)
#
#
# def createFastaFiles(infile, directory):
#     ref_dict = getPickle("{}.pickle".format(infile))
#     # create the directory
#     path_to_dir = "{}/{}".format(os.getcwd(), directory)
#     os.chdir(path_to_dir)
#     for i in ref_dict:
#         sRNA, sequence = ref_dict[i]["sRNA"], ref_dict[i]["sequence"]
#         generateFASTA(sRNA, sequence, i)
#         print(i)
#
#
def main():
    os.chdir('./intaRNA-9-21/')
    with open("sRNA_target_pair_candidates_for_Daniel-Sheet1.csv", 'r') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        # Skip Header
        readCSV.__next__()
        for row in readCSV:
            sRNAname, sRNA, mRNAname, mRNA = row[0], row[1], row[2], row[3]
            generateFASTA(sRNAname, sRNA)
            generateFASTA(mRNAname, mRNA)
if __name__ == '__main__':
    main()
