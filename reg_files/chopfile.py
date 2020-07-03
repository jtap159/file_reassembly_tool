#!/usr/bin/env python
#
# Chop up the input text into 15 character substrings with overlap
import random
import urllib
import sys

sourceText = ""
with open(sys.argv[1], 'r') as f:
    sourceText += f.read()
    srcLen = len(sourceText)
    start = 0
    fragLen = 0
    last = 0
    frags = []
    while last < srcLen:
        fragLen = 15
        frags.append(urllib.quote_plus(sourceText[start:start+fragLen]))
        last = start + fragLen - 1
        offset = random.randint(5, 11)
        start = start+offset
    random.shuffle(frags)
    print "\n".join(frags)
