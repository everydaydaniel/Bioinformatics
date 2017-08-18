import analysis.getAfinityValues as afinity
from analysis.analyze import *
import sequencing.sequenceReading as sequenceReading
import sequencing.acidToDNA as acidToDNA
import analysis.generate_csv as csv_gen

# python 3
# SETUP GLOBALS
# afinity_lookup is the lookup table for mfe/afinity values
afinity_lookup = afinity.mfeDictionary

'''
Currently this main script will look at a sequence and break it up into
6-mers i.e two codon pairs. The afinity_lookup table contains all possible
two codon pair combiniations except for the stop codons. The main script also
moves over the sequence in steps of 3. What I would like to accomplish is
having command line inputs so that you dont have to open the script and
set the input variables. Another challenge is how to do the 200-mer analysis.
will probably be done in a different script.
Desired variables/future TODO:
sequence: either .txt or input, base: either U or T, output filename: self
explanatory, step size/mer-size: here it gets tricky, might want to have a
6-mer analysis script and a separate n-mer script to prepare data.
'''

def main():
    # Read BetaGal.txt and swap base to U bc RNA
    try:
        sequence = sequenceReading.readFile("BetaGal.txt")
        sequence = acidToDNA.swapBase(sequence, "U")
        position = 0
        data_to_write = []
        for i in range(0, len(sequence), 3):
            if i + 6 > len(sequence):
                break
            else:
                # temp is the sub sequence we perform analysis on.
                temp = acidToDNA.CreateSixMer(sequence[i:i + 6], "U")
                itr_num = 0
                # raw sequence values has the mfe lookup value per codon pair
                raw_sequence_values = []
                wildType = temp[0]
                wildType_mfe = afinity_lookup[wildType]
                for six_mer in temp:
                    itr_num += 1
                    current_sequence_mfe = afinity_lookup[six_mer]
                    delta_diff = deltaDiff(wildType_mfe, current_sequence_mfe)
                    energy_diff = energyDiff(wildType_mfe, current_sequence_mfe)
                    raw_sequence_values.append((six_mer, afinity_lookup[six_mer]))

                energy_values = get_energy_values(wildType_mfe, raw_sequence_values)
                max_delta_diff_value = energy_values[0][1]
                max_energy_difference = energy_values[1][0][-1]
                sequences_with_max_energy = [value[0] for value in energy_values[1]]
                # -1 because wildtype is not a mutation
                num_mutations = len(raw_sequence_values) - 1
                signs = getSigns(energy_values[-1])
                positive, negative, zero = signs[0], signs[1], signs[2]
                sequenceString = getSequenceString(sequences_with_max_energy)
                data = "{},{},{},{},{},{},{},{},{},{}".format(
                    position, wildType, wildType_mfe,  max_delta_diff_value,
                    max_energy_difference, sequenceString, num_mutations, positive,
                    negative, zero
                )
                data_to_write.append(data)

                # increment position index
                position += 3
                # print(data)
    # raised Exception from create sixmer due to stop codin check
    except StopIteration:
        position += 3
        # print("End of sequence")
        # print("{}\n{}".format(position, "END"))

        # final row that tells you why the itteration stopped
        data_to_write.append(
            "stop codon encountered: {} at position: {} analysis complete".format(
                sequence[-6:], position))

        # generate the header, header += string is because I didn't want the
        # lines to be too long. Probably a better way but wtvs.
        header = "position , wildType , energy of wildType, "
        header += "max absolute energy difference,"
        header += "max energy difference,sequences with max energy difference,"
        header += "number of mutations,positive,negative,zero"
        # write the data to a csv and complete
        csv_gen.write_csv("betgal_results", data_to_write, header)
        # for future refenernce, get output file name and print location of the
        # csv file.
        print("done.")

if __name__ == '__main__':
    main()
