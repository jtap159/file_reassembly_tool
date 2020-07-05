from urllib.parse import unquote_plus, unquote


def decode_frags(input_file):
    # decode & collect each fragment and remove carrier return /n
    decoded_frags = [unquote(line[:-1]) for line in input_file]
    return decoded_frags


decoded_frags_ordered = ['//+Sample+progr',
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

decoded_frags_shuffled = ['stem.out.printl',
                          'e+terminal+wind',
                          'ain(String[]+ar',
                          's)+{\n++++++++//',
                          'window.\n+++++++',
                          'ello,+World");\n',
                          'println("Hello,',
                          '+class+HelloWor',
                          'rints+"Hello,+W',
                          'c+static+void+m',
                          '//+Sample+progr',
                          'tic+void+main(S',
                          '");\n++++}\n}\n',
                          '++++++++System.',
                          'm\npublic+class+',
                          'ple+program\npub',
                          '++public+static',
                          'ello,+World"+to',
                          '[]+args)+{\n++++',
                          's+HelloWorld+{\n',
                          '+++++//+Prints+',
                          'ld"+to+the+term',
                          'World+{\n++++pub']


def assemble_frags(decoded_frags):
    while len(decoded_frags) > 1:
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
                        matches.append({"frag": frag, "spliced_frag": frag[:-j]})  # remove the overlapping characters so it can be combined with the anchor
                        break
            if num_of_matches == 1:
                decoded_frags.remove(anchor_frag)
                decoded_frags.remove(matches[0]['frag'])
                combine_frags = matches[0]['spliced_frag'] + anchor_frag
                decoded_frags.append(combine_frags)
                break
    return decoded_frags[0]


if __name__ == "__main__":
    # assemble_frags_shuffled = assemble_frags(decoded_frags_shuffled)
    assemble_frags_ordered = assemble_frags(decoded_frags_ordered)
