import analysis.getAfinityValues as afinity
import sequencing.sequenceReading as sequenceReading
import sequencing.acidToDNA as acidToDNA
import analysis.generate_csv as csv_gen


afinity_lookup = afinity.mfeDictionary

'''
This script will prepare the sequence so that it can be used on tacc to
submit sequencees to rna struct.
Notes: the len range and everything else has to be calculated for N length
sequences. header and filename should be a parameter.
'''


def midpointCalc(mer_size):
    midpoint = mer_size // 3
    midpoint = midpoint // 2
    return midpoint * 3


def main():
    # NOTE: FIX THE MER SIZE THING SO THAT IT CORRECTLY SENDS THE RIGHT
    # SUB SEQUENCE INTO THE substitue_N_Mer FUNCTION!!!!
    # psuedo valriables
    # so far input must be grater than 9, so mer_size >= 12.
    mer_size = 198

    try:
        if mer_size % 3 != 0:
            print("requested subsequence length ({}) not divisable by 3".format(mer_size))
            return
        midpoint = midpointCalc(mer_size)
        # read BetaGal sequence and swap the base to U
        sequence = sequenceReading.readFile("BetaGal.txt")
        sequence = acidToDNA.swapBase(sequence, "U")
        # We're gonna start at the midpoint because thats the first position
        # where we can make the wanted subsequence size.
        for i in range(midpoint, len(sequence), 3):
            # break if we reach the end of the sequences we dont get a out of
            # index range error.
            if i + midpoint > len(sequence):
                break

            sub_seq = sequence[i - midpoint:i + midpoint]
            # returned dictionary:
            # { sequences: [list of sequences], wildtype: "wildtype",
            # codons: [list of codon mutations], position : int }
            sub_seq_analysis = acidToDNA.substitue_N_Mer(sub_seq, i)
            # we need to write this to a csv file that can be easily read
            # and written into so we can write the results.
            header = ["position", "wildtype", "amino acid", "condons", "sequences"]
            position = sub_seq_analysis['position']
            wildtype = sub_seq_analysis['wildtype']
            amino = sub_seq_analysis['amino acid']
            codons = csv_gen.listToString(sub_seq_analysis['codons'], delimiter=';')
            sequences = csv_gen.listToString(sub_seq_analysis['sequences'], delimiter=';')
            data = [position, wildtype, amino, codons, sequences]
            csv_gen.writeToCSV("BetaGalPrep", data, header, delimiter=",")

    except Exception as e:
        raise


if __name__ == '__main__':
    main()
