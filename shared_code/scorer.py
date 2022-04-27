# from shared_code import hand
import pydawg
import pathlib
import json
import re
import copy
from py_expression_eval import Parser

def scoreLettres(lang, hnd, word):
    h = copy.deepcopy(hnd)
    word = word.upper()
    D = pydawg.DAWG()
    with open(str(pathlib.Path(__file__).parent) + "/../dict/" + 'ODS7.bin', 'rb') as f:
        D.binload(f.read())

    # Word has letters from the hand?
    lettres = []
    for c in h["lettres"]:
        lettres.append(list(c.keys())[0])
    originalHand = ''.join(lettres)
    lettersInHand = lettres
    for letter in word:
        if letter not in lettersInHand:
            # return func.HttpResponse(f"Invalid move: {word} has letter {letter} not available in the hand {originalHand}.", status_code=400)
            raise Exception(f"Invalid move: {word} needs the letter '{letter}', which is not available in the hand {originalHand}.")
        lettersInHand.remove(letter)

    # Word in dictionary?
    index = D.word2index(word)
    if index is None:
        # return func.HttpResponse(f"Invalid move: {word} not recognized as a valid word in the dictionary.", status_code=400)
        raise Exception(f"Invalid move: {word} not recognized as a valid word in the dictionary.")

    with open(str(pathlib.Path(__file__).parent) + "/" + lang + '.json') as f:
        data = json.load(f)
    points = data["TileSet"]["Points"]
    wordScore = 0
    for c in word:
        wordScore = wordScore + points[c]

    res = {}
    res["word"] = word
    res["score"] = wordScore
    return res

def scoreChiffres(hnd, formula):
    h = copy.deepcopy(hnd)
    numbersInHand = h["chiffres"]["l"]
    matches = re.finditer(r"(\d+)", formula)
    numbersUsed = 0
    for match in matches:
        number = int(match.group())
        if number not in numbersInHand:
            raise Exception(f"Invalid move: {number} not available in remaining hand {numbersInHand}.")
        numbersInHand.remove(number)
        numbersUsed += 1

    parser = Parser()
    f = parser.parse(formula)

    targetNumber = int(h["chiffres"]["n"])
    res = {}
    res["formula"] = formula
    res["delta"] = abs(int(h["chiffres"]["n"]) - f.evaluate({}))
    res["numbersUsed"] = numbersUsed
    return res