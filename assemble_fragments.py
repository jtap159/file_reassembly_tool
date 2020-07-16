import argparse
from urllib.parse import unquote_plus
import tasks

parser = argparse.ArgumentParser(description='Used to reassemble a fragmented file')
parser.add_argument("file", type=str, help='the directory location of the text file with the fragments')

args = parser.parse_args()
with open(args.file, 'r') as file:
    fragments = [unquote_plus(line[:-1]) for line in file]

assembled_fragments = tasks.assemble_frags(fragments)
if type(assembled_fragments) == str:
    print(assembled_fragments)
else:
    for i, solution in enumerate(assembled_fragments):
        print(f"-----------------------Solution {i+1}----------------------------------")
        print(solution)
    print(f"{len(assembled_fragments)} Possible Solutions Found (see solutions above) \n")


