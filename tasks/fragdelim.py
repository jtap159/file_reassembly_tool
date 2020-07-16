

def frag_delimiter(input_file, output_name):
    # add the delimiter ",,, " after each fragment except for the last one
    fragments = [line[:-1] + ",,, " for line in input_file]
    fragments[-1] = fragments[-1][:-4]
    delim_file = open(f"../delim_files/{output_name}", "w")
    delim_file.writelines(fragments)
    delim_file.close()


if __name__ == "__main__":
    file = open("../frag_files/chopfile-frags.txt", "r")
    output = "chopfile-frags_delim.txt"
    frag_delimiter(file, output)
    file.close()
