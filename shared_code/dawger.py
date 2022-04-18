import pydawg
import bz2

with open('dict/ODS7.txt') as f:
    words = f.readlines()
    D = pydawg.DAWG()
    for word in words:
        w = word.replace("\n", "")
        D.add_word_unchecked(w)

with open('ODS7.bin', 'wb') as f:
        f.write(D.bindump())