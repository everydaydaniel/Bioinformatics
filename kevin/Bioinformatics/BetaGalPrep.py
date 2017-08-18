import analysis.getAfinityValues as afinity
from analysis.analyze import *
import sequencing.sequenceReading as sequenceReading
import sequencing.acidToDNA as acidToDNA
import analysis.generate_csv as csv_gen

afinity_lookup = afinity.mfeDictionary

'''
This script will prepare the sequence so that it can be used on tacc to
submit sequencees to rna struct.
Notes: the len range and everything else has to be calculated for N length
sequences.
'''


def main():
    # NOTE: FIX THE MER SIZE THING SO THAT IT CORRECTLY SENDS THE RIGHT
    # SUB SEQUENCE INTO THE substitue_N_Mer FUNCTION!!!!
    # psuedo valriables
    mer_size = 198

    try:
        if mer_size % 3 != 0:
            print("requested subsequence length ({}) not divisable by 3".format(mer_size))
            return
        midpoint = mer_size // 2
        # read BetaGal sequence and swap the base to U
        sequence = sequenceReading.readFile("BetaGal.txt")
        sequence = acidToDNA.swapBase(sequence, "U")
        for i in range(midpoint, len(sequence), 3):
            # break if we reach the end of the sequences we dont get a out of
            # index range error.
            if i + midpoint > len(sequence):
                break
            print()
            sub_seq = sequence[i - midpoint:i + midpoint]
            acidToDNA.substitue_N_Mer(sub_seq)
            print()
            print()

    except Exception as e:
        raise


if __name__ == '__main__':
    main()
