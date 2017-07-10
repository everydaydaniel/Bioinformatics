def countPersonal():
    personal = []
    with open('AffinitySequences.txt', 'r') as f:
        count = 0
        for line in f:

            if line.strip():
                count += 1
                personal.append(line.strip())
                # print(line.strip())
        return count, personal


def countOther():
    other = []
    with open('resultsfile.txt', 'r') as f:
        count = 0
        for line in f:
            line = line.split('.')[0].strip()
            count += 1
            other.append(line.strip())
            # print(line)
        return count, other


def main():
    with open("remainingCodons.txt", 'r') as f:
        for line in f:
            if line.strip():
                line = line.strip()
                fname = "{}".format(line)
                outfile = open(fname, 'w')
                preparedFile = "2\nUCCUCCAC\n{}\n1 2".format(line)
                outfile.write(preparedFile)
                outfile.close()


if __name__ == '__main__':
    main()
