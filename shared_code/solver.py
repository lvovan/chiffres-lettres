from shared_code import hand
import pydawg
import pathlib
import copy

def lettresSolver(D, letters, prefix = "", longestWord = ""):
    for letter in letters:
        remainingLetters = letters.copy()
        remainingLetters.remove(letter)
        newPrefix = prefix + letter

        if D.word2index(newPrefix) is not None:
            # This is a working word
            if len(newPrefix) > len(longestWord):
                longestWord = newPrefix

        if sum(1 for _ in D.find_all(newPrefix)) > 1:
            # Prefix can lead to something
            exploration = lettresSolver(D, remainingLetters, newPrefix, longestWord)
            if len(exploration) > len(longestWord):
                longestWord = exploration

    return longestWord

# https://github.com/imanuch/dcdl
def chiffresCalculs(a,i,j,n):
    liste = []
    for nbr in range(len(a)):
        liste.append(a[nbr])

    if n == 0:
        liste.append(liste[i]*liste[j])
        del liste[j]
        del liste[i]

    elif n == 1 and liste[j]!=0:
        liste.append(liste[i]/liste[j])
        del liste[j]
        del liste[i]

    elif n == 2:
        liste.append(liste[i]+liste[j])
        del liste[j]
        del liste[i]
    elif n == 3:
        liste.append(liste[i]-liste[j])
        del liste[j]
        del liste[i]
    elif n == 4:
        liste.append(liste[j]-liste[i])
        del liste[j]
        del liste[i]
    elif n == 5 and liste[i]!=0:
        liste.append(liste[j]/liste[i])
        del liste[j]
        del liste[i]
    return liste


def chiffresSolver(res, n, liste):
    cal = ["*","/","+","-","-","/"]
    if n in liste:
        return True
    if 0 in liste:
        return False
    for i in range(len(liste)-1):
        for j in range(i+1,len(liste)):
            for k in range(6):
                if chiffresSolver(res, n,chiffresCalculs(liste,i,j,k)):
                    if k<4:
                        res.append(f"{liste}{liste[i]}{cal[k]}{liste[j]} = {chiffresCalculs(liste,i,j,k)[-1]}")
                    else:
                        res.append(f"{liste}{liste[j]}{cal[k]}{liste[i]} = {chiffresCalculs(liste,i,j,k)[-1]}")
                    return True
    return False

def solver():
    h = hand.hand()
    res = {}
    res["main"] = h

    # Lettres
    D = pydawg.DAWG()
    with open(str(pathlib.Path(__file__).parent) + "/../dict/" + 'ODS7.bin', 'rb') as f:
        D.binload(f.read())
    longestWord = lettresSolver(D, h["lettres"])
    res["lettres"] = {}
    res["lettres"]["word"] = longestWord
    res["lettres"]["score"] = len(longestWord)

    # Chiffres
    res["chiffres"] = []
    chiffresSolver(res["chiffres"], h["chiffres"]["n"], h["chiffres"]["l"])

    return res