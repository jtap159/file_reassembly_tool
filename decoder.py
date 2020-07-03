from urllib.parse import unquote_plus

encoded_slice = '%2F%2FSample+prograe+program%0Apubli'

file = open("frag_files/hello-ordered-frags.txt", "r")
slices = [unquote_plus(line[:-1]) for line in file]
file.close()

if __name__ == "__main__":
    decoded_slice = unquote_plus(encoded_slice)