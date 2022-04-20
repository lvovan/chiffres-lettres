import logging
from os import stat
from shared_code import hand, scorer
import json
import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    bodyJson = req.get_json()
    name = bodyJson.get("nom")
    group = bodyJson.get("groupe")
    word = bodyJson.get("mot")
    formula = bodyJson.get("formule")
    h = hand.hand()

    try:
        resLettres = scorer.scoreLettres(h, word)
        resChiffres = scorer.scoreChiffres(h, formula)
    except Exception as e:
        return func.HttpResponse(str(e), status_code=400)

    
    res = {}
    res["joueur"] = { "nom": name, "groupe": group }
    res["hand"] = h
    res["lettres"] = resLettres
    res["chiffres"] = resChiffres

    return func.HttpResponse(json.dumps(res), mimetype="application/json")