import argparse
from urllib.parse import unquote_plus
from tasks.reassemble import assemble_frags

parser = argparse.ArgumentParser(description='Used to reassemble a fragmented file')
parser.add_argument("file", type=str, help='the directory location of the text file with the fragments')

args = parser.parse_args()
with open(args.file, 'r') as file:
    fragments = [unquote_plus(line[:-1]) for line in file]

assemble_frags = assemble_frags(fragments)
if type(assemble_frags) == str:
    print(assemble_frags)
else:
    for i, solution in enumerate(assemble_frags):
        print(f"-----------------------Solution {i+1}----------------------------------")
        print(solution)
    print(f"{len(assemble_frags)} Possible Solutions Found (see solutions above) \n")
