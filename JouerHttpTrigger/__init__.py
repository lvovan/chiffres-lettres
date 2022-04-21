import logging
from os import stat
from shared_code import hand, scorer
import json
import os
import re
from datetime import datetime
from azure.storage.blob import ContainerClient

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    bodyJson = req.get_json()
    name = bodyJson.get("nom")
    group = bodyJson.get("groupe")
    word = bodyJson.get("mot")
    formula = bodyJson.get("formule")
    h = hand.hand()

    # Check name and group validity
    if not re.fullmatch("^[A-Za-z0-9\-]{1,32}$", name):
        func.HttpResponse("'name' must be alphanumeric only, no spaces and up to 32 characters", status_code=422)
    if not re.fullmatch("^[A-Za-z0-9\-]{0,32}$", group):
        func.HttpResponse("'group' must be empty or alphanumeric only, no spaces and up to 32 characters", status_code=422)

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
    container_client.upload_blob(f"{strDate}.{group}.{name}.json", resJson)

    return func.HttpResponse(resJson, mimetype="application/json")