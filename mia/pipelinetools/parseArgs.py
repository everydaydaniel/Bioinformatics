import argparse


def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="Input the path of the file you want to create a matrix for")
    parser.add_argument("--start", type=int, help="Starting coulumn for the bed file.")
    parser.add_argument("--end", type=int, help="Ending coulumn for the bed file.")
    args = parser.parse_args()
    return args
