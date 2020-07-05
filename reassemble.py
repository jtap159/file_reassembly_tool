from urllib.parse import unquote_plus, unquote
from operator import itemgetter
import pandas as pd


def decode_frags(input_file):
    decoded_frags = []
    anchor_frag_index = None
    for i, line in enumerate(input_file):
        decoded_frag = unquote(line[:-1])  # decode & collect each fragment and remove carrier return /n
        decoded_frags.append(decoded_frag)
        if len(decoded_frag) < 15:  # check for a right anchor point with a frag less than 15 characters
            anchor_frag_index = i
    return decoded_frags, anchor_frag_index


decoded_frags = ['//+Sample+progr',
                 'program\npublic+',
                 'ublic+class+Hel',
                 'lass+HelloWorld',
                 'elloWorld+{\n+++',
                 'd+{\n++++public+',
                 'public+static+v',
                 'c+static+void+m',
                 'id+main(String[',
                 '(String[]+args)',
                 'args)+{\n+++++++',
                 '++++++//+Prints',
                 '//+Prints+"Hell',
                 'ts+"Hello,+Worl',
                 ',+World"+to+the',
                 '"+to+the+termin',
                 'rminal+window.\n',
                 'ow.\n++++++++Sys',
                 '+++++++System.o',
                 'stem.out.printl',
                 'intln("Hello,+W',
                 'o,+World");\n+++',
                 'rld");\n++++}\n}\n',
                 ';\n++++}\n}\n']

anchor_frag = decoded_frags.pop()
num_of_frags = len(decoded_frags)
assembled_string = anchor_frag
for j in range(0, num_of_frags):
    frag = decoded_frags[-1]
    for i in range(len(anchor_frag), 2, -1):
        if frag[-i:] == anchor_frag[:i]:
            assembled_string = frag[:-i] + assembled_string
            anchor_frag = decoded_frags.pop()
            break


if __name__ == "__main__":
    file = open("frag_files/hello-ordered-frags.txt", "r")
    decoded_frags, anchor_frag_index = decode_frags(file)
    file.close()
    # max(d1.items(), key=itemgetter(1))[0]
