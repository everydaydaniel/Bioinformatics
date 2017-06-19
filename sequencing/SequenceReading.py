import argparse
import sys


# Sequence reading module. Use to prepare strings for AcidToDNA
# module.
def readFile(infile, outfile):
    try:
        # check so that you don't tab complete and delete a script. Honestly
        # this is just an irrational fear of mine.
        if outfile.endswith('.py'):
            raise NameError

        sequence = ""
        with open(infile, 'r') as f:
            for line in f:
                sequence += line.strip().upper()
        return sequence

    # Exception block
    # ===============
    except IndexError as e:
        return "Not enough arguments given.\nNeed <infile> and <outfile>"
    except NameError as e:
        return "Outfile is a script, please use *.txt or any other format."
    except FileNotFoundError as e:
        return e,
    # ===============


def main():
    # parse arguments.
    parser = argparse.ArgumentParser(description="Set infiles and settings.")
    parser.add_argument('-i', "--infile", required=True,
                        type=argparse.FileType('r'), metavar='', dest="infile",
                        help="Infile that contains a sequence.")

    parser.add_argument('-o', "--outfile", type=argparse.FileType('w'),
                        metavar='', dest="outfile",
                        help="Outfile to write results into. If no name is given defualt will\
                        be <infile>.out.txt")
    args = parser.parse_args()

    # if no outfile is given, set it to infile.out
    try:
        outfile = args.outfile.name
    except AttributeError as e:
        name = args.infile.name.split('.')
        outfile = name[0] + ".out"

    print(readFile(args.infile.name, outfile))


if __name__ == '__main__':
    main()
