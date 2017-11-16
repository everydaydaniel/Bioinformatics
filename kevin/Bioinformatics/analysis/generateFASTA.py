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


# def createFastaFilesFromDict(infile, directory):
#     ref_dict = getPickle("{}.pickle".format(infile))
#     # create the directory
#     path_to_dir = "{}/{}".format(os.getcwd(), directory)
#     os.chdir(path_to_dir)
#     for i in ref_dict:
#         sRNA, sequence = ref_dict[i]["sRNA"], ref_dict[i]["sequence"]
#         generateFASTA(sRNA, sequence, i)
#         print(i)

#
# def main():
#     path_to_dir = "{}/FastaFilesWithInteracting".format(os.getcwd())
#     os.chdir(path_to_dir)
#     for fname in os.listdir("."):
#         name, ext = os.path.splitext(fname)
#         name = name.replace(" ", "")
#         newName = "{}{}".format(name, ext)
#         print(fname, newName)
#         os.rename(fname, newName)
