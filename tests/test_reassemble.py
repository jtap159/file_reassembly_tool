from urllib.parse import unquote_plus
import tasks

hello_frags = ['// Sample program\npublic class HelloWorld {\n    public static void main(String[] args) {\n        // '
               'Prints "Hello, World" to the terminal window.\n        System.out.println("Hello, World");\n    }\n}\n']

ipsumlorem_short_frags = ['Non eram nescius, Brute, cum, quae summis ingeniis exquisitaque doctrina philosophi '
                          'Graeco\nsermone tractavissent, ea Latinis litteris mandaremus, fore ut hic noster labor '
                          'in varias\nreprehensiones incurreret. nam quibusdam, et iis quidem non admodum indoctis, '
                          'totum hoc\ndisplicet philosophari. quidam autem non tam id reprehendunt, si remissius '
                          'agatur, sed tantum\nstudium tamque multam operam ponendam in eo non arbitrantur. erunt '
                          'etiam, et ii quidem eruditi\nGraecis litteris, contemnentes Latinas, qui se dicant in '
                          'Graecis legendis operam malle consumere.\npostremo aliquos futuros suspicor, qui me ad '
                          'alias litteras vocent, genus hoc scribendi, etsi sit\nelegans, personae tamen et '
                          'dignitatis esse negent.\nContra quos omnis dicendum breviter existimo. Quamquam '
                          'philosophiae quidem vituperatoribus satis\nresponsum est eo libro, quo a nobis philosophia '
                          'defensa et collaudata est, cum esset accusata et\nvituperata ab Hortensio. qui liber cum '
                          'et tibi probatus videretur et iis, quos ego posse iudicare\narbitrarer, plura suscepi '
                          'veritus ne movere hominum studia viderer, retinere non posse. Qui autem,\nsi maxime hoc '
                          'placeat, moderatius tamen id volunt fieri, difficilem quandam temperantiam postulant\nin '
                          'eo, quod semel admissum coerceri reprimique non potest, ut propemodum iustioribus utamur '
                          'illis,\nqui omnino avocent a philosophia, quam his, qui rebus infinitis modum constituant '
                          'in reque eo meliore,\nquo maior sit, mediocritatem desiderent.\n']

shake_frags = ["The quality of mercy is not strain'd,\nIt droppeth as the gentle rain from heaven\nUpon the place "
               "beneath: it is twice blest;\nIt blesseth him that gives and him that takes:\n'Tis mightiest in the "
               "mightiest: it becomes\nThe throned monarch better than his crown;\nHis sceptre shows the force of "
               "temporal power,\nThe attribute to awe and majesty,\nWherein doth sit the dread and fear of kings;\nBut "
               "mercy is above this sceptred sway;\nIt is enthroned in the hearts of kings,\nIt is an attribute to "
               "God himself;\nAnd earthly power doth then show likest God's\nWhen mercy seasons justice. Therefore, "
               "Jew,\nThough justice be thy plea, consider this,\nThat, in the course of justice, none of us\nShould "
               "see salvation: we do pray for mercy;\nAnd that same prayer doth teach us all to render\nThe deeds of "
               "mercy. I have spoke thus much\nTo mitigate the justice of thy plea;\nWhich if thou follow, this strict "
               "court of Venice\nMust needs give sentence 'gainst the merchant there."]

chop_frags = ['#!/usr/bin/env python\n#\n# Chop up the input text into 15 character substrings with overlap\nimport '
              'random\nimport urllib\nimport sys\n\nsourceText = ""\nwith open(sys.argv[1], \'r\') as f:\n    '
              'sourceText += f.read()\n    srcLen = len(sourceText)\n    start = 0\n    fragLen = 0\n    last = 0\n    '
              'frags = []\n    while last < srcLen:\n        fragLen = 15\n        '
              'frags.append(urllib.quote_plus(sourceText[start:start+fragLen]))\n        '
              'last = start + fragLen - 1\n        offset = random.randint(5, 11)\n        '
              'start = start+offset\n    random.shuffle(frags)\n    print "\\n".join(frags)\n']


def test_assemble_frags():
    with open("frag_files/hello-ordered-frags.txt", 'r') as file:
        fragments = [unquote_plus(line[:-1]) for line in file]
    assert tasks.assemble_frags(fragments) == hello_frags[0]

    with open("frag_files/hello-frags.txt", 'r') as file:
        fragments = [unquote_plus(line[:-1]) for line in file]
    assert tasks.assemble_frags(fragments) == hello_frags[0]

    with open("frag_files/IpsumLorem-short-frags.txt", 'r') as file:
        fragments = [unquote_plus(line[:-1]) for line in file]
    assert tasks.assemble_frags(fragments) == ipsumlorem_short_frags[0]

    with open("frag_files/Shake-frags.txt", 'r') as file:
        fragments = [unquote_plus(line[:-1]) for line in file]
    assert tasks.assemble_frags(fragments) == shake_frags[0]

    with open("frag_files/chopfile-frags.txt", 'r') as file:
        fragments = [unquote_plus(line[:-1]) for line in file]
    assemble_fragments = tasks.assemble_frags(fragments)
    assert assemble_fragments[5] == chop_frags[0] and len(assemble_fragments) == 17
