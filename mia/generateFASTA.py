from heatMapping import *
import os


def generateFASTA(sRNA, sequence, number):
    with open("{}.fasta".format(sRNA), 'w') as outfile:
        sRNA, sequence = sRNA.strip(), sequence.strip()
        toWrite = ">{}-{}\n{}".format(number, sRNA, sequence)
        print(toWrite)
        outfile.write(toWrite)


def createFastaFiles(infile, directory):
    ref_dict = getPickle("{}.pickle".format(infile))
    # create the directory
    path_to_dir = "{}/{}".format(os.getcwd(), directory)
    os.chdir(path_to_dir)
    for i in ref_dict:
        sRNA, sequence = ref_dict[i]["sRNA"], ref_dict[i]["sequence"]
        generateFASTA(sRNA, sequence, i)
        print(i)


def main():
    path_to_dir = "{}/FastaFilesWithInteracting".format(os.getcwd())
    os.chdir(path_to_dir)
    for fname in os.listdir("."):
        name, ext = os.path.splitext(fname)
        name = name.replace(" ", "")
        newName = "{}{}".format(name, ext)
        print(fname, newName)
        os.rename(fname, newName)

if __name__ == '__main__':
    main()
