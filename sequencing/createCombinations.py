import argparse
import sequenceReading
import acidToDNA


def main():

    # parse arguments.
    # ==========================================================================
    parser = argparse.ArgumentParser(description="Set infiles and settings.")
    parser.add_argument('-i', "--infile", required=True,
                        type=argparse.FileType('r'), metavar='', dest="infile",
                        help="Infile that contains a sequence.")

    parser.add_argument('-o', "--outfile", type=argparse.FileType('w'),
                        metavar='', dest="outfile",
                        help="Outfile to write results into. If no name is given defualt will\
                        be <infile>.out.txt")
    parser.add_argument('-b', '--base', type=str, required=False,
                        default="T", help="Choose base, either T or U", metavar='')
    args = parser.parse_args()
    infile = args.infile.name
    # if no outfile is given, set it to infile.out
    try:
        outfile = args.outfile.name
    except AttributeError as e:
        name = args.infile.name.split('.')
        outfile = name[0] + ".out"

    # Create Sequence
    sequence = sequenceReading.readFile(infile, outfile)
    # Swap base
    sequence = acidToDNA.swapBase(sequence, args.base)

    # Main loop
    start_idx = 10
    for i in range(0, len(sequence), 3):
        if i + 6 > len(sequence):
            break
        else:
            start_idx += 3
            temp = acidToDNA.CreateSixMer(sequence[i:i + 6], args.base)
            itr_num = 0
            for six_mer in temp:
                itr_num += 1
                new_sequence = "{}{}{}".format(sequence[:i], six_mer, sequence[i + 6:])
                print("{}:{}\n{}".format(start_idx, itr_num, six_mer))
            print()

if __name__ == '__main__':
    main()
