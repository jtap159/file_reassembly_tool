import reassemble

hello_frags_string = ['//+Sample+program\npublic+class+HelloWorld+{\n++++public+static+void+main(String[]+args)+{\n++'
                      '++++++//+Prints+"Hello,+World"+to+the+terminal+window.\n++++++++System.out.println("Hello,'
                      '+World");\n++++}\n}\n']


def test_assemble_frags():
    shuffled_file = open("frag_files/hello-frags.txt", "r")
    assert reassemble.assemble_frags(shuffled_file) == hello_frags_string
    shuffled_file.close()