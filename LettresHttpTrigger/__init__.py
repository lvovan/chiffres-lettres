import logging
import json
from shared_code import hand
import azure.functions as func
import pydawg
import pathlib

def main(req: func.HttpRequest) -> func.HttpResponse:
    bodyJson = req.get_json()
    name = bodyJson.get("name")
    word = bodyJson.get("word").upper()
    h = hand.hand()

    D = pydawg.DAWG()
    with open(str(pathlib.Path(__file__).parent) + "/../dict/" + 'ODS7.bin', 'rb') as f:
        D.binload(f.read())

    # Word has letters from the hand?
    originalHand = str(h["lettres"])
    lettersInHand = h["lettres"]
    for letter in word:
        if letter not in lettersInHand:
            return func.HttpResponse(f"Invalid move: {word} has letter {letter} not available in the hand {originalHand}.", status_code=400)
        lettersInHand.remove(letter)

    # Word in dictionary?
    index = D.word2index(word)
    if index is None:
        return func.HttpResponse(f"Invalid move: {word} not recognized as a valid word in the dictionary.", status_code=400)

    res = {}
    res["name"] = name
    res["word"] = word
    res["score"] = len(word)


    return func.HttpResponse(json.dumps(res))