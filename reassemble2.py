
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

all_best_matches = []
for k in range(0, len(decoded_frags)):  # use every fragment as an anchor and check for how many matches they have, left
    temp_decoded_frags = decoded_frags.copy()
    anchor_frag = temp_decoded_frags.pop(k)
    max_overlap = 14 if len(anchor_frag) == 15 else len(anchor_frag)
    num_of_matches = 0
    matches = []
    for i, frag in enumerate(temp_decoded_frags):  # check every fragment to see if they fit to the anchor fragment
        for j in range(max_overlap, 2, -1):
            if frag[-j:] == anchor_frag[:j]:  # match left
                num_of_matches += 1
                matches.append(frag[:-j])  # remove the overlapping characters so it can be combined with the anchor
                break
    if num_of_matches == 1:
        combine_frags = matches[0] + anchor_frag
        all_best_matches.append(combine_frags)


if __name__ == "__main__":
    pass
