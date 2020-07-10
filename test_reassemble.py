import reassemble

hello_ordered_frags = ['//+Sample+program\npublic+class+HelloWorld+{\n++++public+static+void+main(String[]+args)'
                       '+{\n+++++++//+Prints+"Hello,+World"+to+the+terminal+window.\n++++++++System.out.println'
                       '("Hello,+World");\n++++}\n}\n']

hello_frags = ['//+Sample+program\npublic+class+HelloWorld+{\n++++public+static+void+main(String[]+args)+{\n++'
               '++++++//+Prints+"Hello,+World"+to+the+terminal+window.\n++++++++System.out.println("Hello,'
               '+World");\n++++}\n}\n']

ipsumlorem_short_frags = ['Non+eram+nescius,+Brute,+cum,+quae+summis+ingeniis+exquisitaque+doctrina+philosophi'
                          '+Graeco\nsermone+tractavissent,+ea+Latinis+litteris+mandaremus,+fore+ut+hic+noster+'
                          'labor+in+varias\nreprehensiones+incurreret.+nam+quibusdam,+et+iis+quidem+non+admodum+'
                          'indoctis,+totum+hoc\ndisplicet+philosophari.+quidam+autem+non+tam+id+reprehendunt,+si'
                          '+remissius+agatur,+sed+tantum\nstudium+tamque+multam+operam+ponendam+in+eo+non+'
                          'arbitrantur.+erunt+etiam,+et+ii+quidem+eruditi\nGraecis+litteris,+contemnentes+'
                          'Latinas,+qui+se+dicant+in+Graecis+legendis+operam+malle+consumere.\npostremo+aliquos+'
                          'futuros+suspicor,+qui+me+ad+alias+litteras+vocent,+genus+hoc+scribendi,+etsi+'
                          'sit\nelegans,+personae+tamen+et+dignitatis+esse+negent.\nContra+quos+omnis+dicendum+'
                          'breviter+existimo.+Quamquam+philosophiae+quidem+vituperatoribus+satis\nresponsum+est+'
                          'eo+libro,+quo+a+nobis+philosophia+defensa+et+collaudata+est,+cum+esset+accusata+'
                          'et\nvituperata+ab+Hortensio.+qui+liber+cum+et+tibi+probatus+videretur+et+iis,+quos+'
                          'ego+posse+iudicare\narbitrarer,+plura+suscepi+veritus+ne+movere+hominum+studia+'
                          'viderer,+retinere+non+posse.+Qui+autem,\nsi+maxime+hoc+placeat,+moderatius+tamen+id+'
                          'volunt+fieri,+difficilem+quandam+temperantiam+postulant\nin+eo,+quod+semel+admissum+'
                          'coerceri+reprimique+non+potest,+ut+propemodum+iustioribus+utamur+illis,\nqui+omnino+'
                          'avocent+a+philosophia,+quam+his,+qui+rebus+infinitis+modum+constituant+in+reque+eo+'
                          'meliore,\nquo+maior+sit,+mediocritatem+desiderent.\n']

shake_frags = ["The+quality+of+mercy+is+not+strain'd,\nIt+droppeth+as+the+gentle+rain+from+heaven\nUpon+the+place+"
               "beneath:+it+is+twice+blest;\nIt+blesseth+him+that+gives+and+him+that+takes:\n'Tis+mightiest+in+the+"
               "mightiest:+it+becomes\nThe+throned+monarch+better+than+his+crown;\nHis+sceptre+shows+the+force+of+"
               "temporal+power,\nThe+attribute+to+awe+and+majesty,\nWherein+doth+sit+the+dread+and+fear+of+kings;\nBut+"
               "mercy+is+above+this+sceptred+sway;\nIt+is+enthroned+in+the+hearts+of+kings,\nIt+is+an+attribute+to+God+"
               "himself;\nAnd+earthly+power+doth+then+show+likest+God's\nWhen+mercy+seasons+justice.+Therefore,+"
               "Jew,\nThough+justice+be+thy+plea,+consider+this,\nThat,+in+the+course+of+justice,+none+of+us\nShould+"
               "see+salvation:+we+do+pray+for+mercy;\nAnd+that+same+prayer+doth+teach+us+all+to+render\nThe+deeds+of+"
               "mercy.+I+have+spoke+thus+much\nTo+mitigate+the+justice+of+thy+plea;\nWhich+if+thou+follow,+this+"
               "strict+court+of+Venice\nMust+needs+give+sentence+'gainst+the+merchant+there."]

hello_ordered_frags[0] = hello_ordered_frags[0].replace("+", " ")
hello_frags[0] = hello_frags[0].replace("+", " ")
ipsumlorem_short_frags[0] = ipsumlorem_short_frags[0].replace("+", " ")
shake_frags[0] = shake_frags[0].replace("+", " ")


def test_assemble_frags():
    file = open("frag_files/hello-ordered-frags.txt", "r")
    assert reassemble.assemble_frags(file) == hello_ordered_frags
    file.close()
    file = open("frag_files/hello-frags.txt", "r")
    assert reassemble.assemble_frags(file) == hello_frags
    file.close()
    file = open("frag_files/IpsumLorem-short-frags.txt", "r")
    assert reassemble.assemble_frags(file) == ipsumlorem_short_frags
    file.close()
    file = open("frag_files/Shake-frags.txt", "r")
    assert reassemble.assemble_frags(file) == shake_frags
    file.close()
