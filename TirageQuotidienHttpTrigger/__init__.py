from datetime import datetime
import random
import json
import logging
import string
import pathlib

import azure.functions as func

def chiffres():
    bag = []
    for i in range(1, 10):
        bag.append(i)
    bag += [25, 50, 75, 100]
    hand = []
    random.seed(a=datetime.utcnow().strftime("%Y%m%d"), version=2)
    for i in range(0, 6):        
        hand.append(bag[random.randrange(0, len(bag))])
    return random.randint(101, 999), hand

def lettres(lang, letterCount):
    bag =[]
    with open(str(pathlib.Path(__file__).parent) + "/" + lang + '.json') as f:
        data = json.load(f)
    distribution = data["TileSet"]["Distribution"]
    for k in distribution:
        if k != "*":
            for i in range(0, distribution[k]):
                bag.append(k)    
    hand = []
    random.seed(a=datetime.now().strftime("%Y%m%d"), version=2)
    for i in range(0, letterCount):        
        hand.append(bag[random.randrange(0, len(bag))])
    return hand

def main(req: func.HttpRequest) -> func.HttpResponse:
    hand = {}
    c = chiffres()
    hand["chiffres"] = { "n":  c[0], "l": c[1]}
    hand["lettres"] = lettres("fr", 9)
    return func.HttpResponse(json.dumps(hand), mimetype="application/json")