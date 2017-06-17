import sys


# Sequence reading module. Use to prepare strings for AcidToDNA
# module.
def readFile():
    args = sys.argv
    try:
        # set files up
        infile = args[1]
        outfile = args[2]
        # check so that you don't tab complete and delete a script. Honestly
        # this is just an irrational fear of mine.
        if outfile.endswith('.py'):
            raise NameError

        sequence = ""
        with open(infile, 'r') as f:
            for line in f:
                sequence += line.strip().upper()

    # Exception block
    except IndexError as e:
        print("Not enough arguments given.\nNeed <infile> and <outfile>")
    except NameError as e:
        print("Outfile is a script, please use *.txt or any other format.")
    except FileNotFoundError as e:
        print(e)


if __name__ == '__main__':
    readFile()
