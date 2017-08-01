import analysis.getAfinityValues as afinity
from analysis.analyze import *
import sequencing.sequenceReading as sequenceReading
import sequencing.acidToDNA as acidToDNA
import analysis.generate_csv as csv_gen


# SETUP GLOBALS
# afinity_lookup is the lookup table for mfe/afinity values
afinity_lookup = afinity.mfeDictionary


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
                # print("sequence", sequence[i:i + 6])
                # delete print("Entering CreateSixMer")
                temp = acidToDNA.CreateSixMer(sequence[i:i + 6], "U")
                # delete print("Exiting CreateSixMer")
                # delete print("sixmer list: {}".format(temp))
                itr_num = 0
                raw_sequence_values = []
                wildType = temp[0]
                wildType_mfe = afinity_lookup[wildType]
                for six_mer in temp:
                    itr_num += 1
                    current_sequence_mfe = afinity_lookup[six_mer]
                    delta_diff = deltaDiff(wildType_mfe, current_sequence_mfe)
                    energy_diff = energyDiff(wildType_mfe, current_sequence_mfe)
                    raw_sequence_values.append((six_mer, afinity_lookup[six_mer]))
                    # print("\n{}:{}\n{}".format(position, itr_num, six_mer))
                    # print("mfe lookup value: {}".format(afinity_lookup[six_mer]))
                    # print("deltaDiff = | {} - {} | = {}".format(wildType_mfe,
                    #                                             current_sequence_mfe, deltaDiff(wildType_mfe, current_sequence_mfe)))
                    # print("sequece: {} deltaDiff: {} energyDiff: {}".format(
                    #     six_mer, delta_diff, energy_diff))
                energy_values = get_energy_values(wildType_mfe, raw_sequence_values)
                max_delta_diff_value = energy_values[0][1]
                max_energy_difference = energy_values[-1][0][-1]
                sequences_with_max_energy = [value[0] for value in energy_values[-1]]
                num_mutations = len(raw_sequence_values)
                signs = getSigns(raw_sequence_values)
                positive, negative, zero = signs[0], signs[1], signs[2]
                sequenceString = getSequenceString(sequences_with_max_energy)
                # print("max delta diff: {} max energy difference values: {}".format(
                #    energy_values[0], energy_values[1]))

                # print("Number of mutations: {}".format(len(raw_sequence_values)))

                # print("positive: {} negative: {} zero: {}".format(signs[0], signs[1], signs[2]))
                # print()
                # increment position index

                # print("\ncondon position: {} \nwildType: {}\nwildType mfe: {}
                # \nenergy_values: {}, \nsigns: {}".format(
                #    position, wildType, wildType_mfe, energy_values, signs))

                data = "{},{},{},{},{},{},{},{},{},{}".format(
                    position, wildType, wildType_mfe,  max_delta_diff_value,
                    max_energy_difference, sequenceString, num_mutations, positive,
                    negative, zero
                )
                data_to_write.append(data)
                position += 3
                # print(data)
    # raised Exception from create sixmer due to stop codin check
    except StopIteration:
        position += 3
        # print("End of sequence")
        # print("{}\n{}".format(position, "END"))
        data_to_write.append(
            "stop codon encountered: {} at position: {} analysis complete".format(
                sequence[-6:], position))
        header = "position , wildType , energy of wildType, "
        header += "max absolute energy difference,"
        header += "max energy difference,sequences with max energy difference,"
        header += "number of mutations,positive,negative,zero"
        csv_gen.write_csv("betgal_results", data_to_write, header)

if __name__ == '__main__':
    main()
