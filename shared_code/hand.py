from datetime import datetime
from operator import le
import random
import json
import pathlib

def chiffres(group):
    bag = []
    for i in range(1, 10):
        bag.append(i)
    bag += [25, 50, 75, 100]
    hand = []
    random.seed(a=datetime.utcnow().strftime("%Y%m%d") + group, version=2)
    for i in range(0, 6):        
        hand.append(bag[random.randrange(0, len(bag))])
    return random.randint(101, 999), hand

def lettres(lang, letterCount, minVowels, minConsonants, group):
    vowels = ["A", "E", "I", "O", "U", "Y"]
    consonantsBag = []
    vowelsBag = []
    with open(str(pathlib.Path(__file__).parent) + "/" + lang + '.json') as f:
        data = json.load(f)
    distribution = data["TileSet"]["Distribution"]
    for k in distribution:
        if k != "*":
            if k in vowels:
                for i in range(0, distribution[k]):
                    vowelsBag.append(k)
            else:
                for i in range(0, distribution[k]):
                    consonantsBag.append(k)

    hand = []

    random.seed(a=datetime.utcnow().strftime("%Y%m%d") + group, version=2)
    # random.seed(a=datetime.utcnow().strftime("%Y%m%d%H%M%s"), version=2)
    points = data["TileSet"]["Points"]
    for i in range(0, minVowels):
        vowel = vowelsBag[random.randrange(0, len(vowelsBag))]
        hand.append(makeTile(points, vowel))
        vowelsBag.remove(vowel)
    for i in range(0, minConsonants):
        consonant = consonantsBag[random.randrange(0, len(consonantsBag))]
        hand.append(makeTile(points, consonant))
        consonantsBag.remove(consonant)
    bag = vowelsBag + consonantsBag
    for i in range(0, letterCount - minVowels - minConsonants):
        letter = bag[random.randrange(0, len(bag))]
        hand.append(makeTile(points, letter))
        bag.remove(letter)

    random.shuffle(hand)
    return hand

def makeTile(points, letter):
    tile = {}
    tile[letter] = points[letter]
    return tile

def hand(groupName = ''):
    if groupName is None:
        groupName = ''
    hand = {}
    c = chiffres(groupName)
    hand["chiffres"] = { "n":  c[0], "l": c[1]}
    hand["lettres"] = lettres("fr", 9, 2, 2, groupName)
    return hand