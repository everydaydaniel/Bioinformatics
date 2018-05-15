originalFile = "reference_seq_Hfq.fa"  # put the messed up one here: Ex probe-24 305
newFile = "reference_seq_Hfq_clean.fa"  # put what you want the name of the new file here
# IMPORTANT: newfile has to be a NEW name!!!!
with open(originalFile, "r") as originalFile:
    with open(newFile, "w") as newFile:
        for line in originalFile:
            if line[0] == ">":
                line = line.split(" ")[0]
                line = line.strip() + "\n"
            newFile.write(line)
