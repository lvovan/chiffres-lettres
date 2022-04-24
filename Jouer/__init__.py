import logging
from os import stat
from shared_code import hand, scorer, validators
import json
import os
import re
from datetime import datetime
from azure.storage.blob import ContainerClient

import azure.functions as func

import shared_code

def main(req: func.HttpRequest) -> func.HttpResponse:
    bodyJson = req.get_json()
    name = bodyJson.get("nom")
    group = bodyJson.get("groupe")
    word = bodyJson.get("mot")
    formula = bodyJson.get("formule")
    h = hand.hand()

    ngValidation = validators.areNameGroupValid(name, group)
    if ngValidation != None:
        return func.HttpResponse(ngValidation, status_code=422)

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
    resJson = json.dumps(res)

    # Store
    containerName="chiffres-lettres-games"
    blobConnString = os.environ['AzureWebJobsStorage']
    container_client = ContainerClient.from_connection_string(conn_str=blobConnString, container_name=containerName)
    try:
        container_client.create_container()
    except:
        None
    strDate = datetime.now().strftime("%Y%m%d")
    container_client.upload_blob(f"{strDate}.{group}.{name}.json", resJson, overwrite=True)

    return func.HttpResponse(resJson, mimetype="application/json")