import logging
import json
import os
import re
import itertools
from datetime import datetime, timedelta
from shared_code import validators
from azure.storage.blob import ContainerClient

import azure.functions as func

def peek(iterable):
    try:
        first = next(iterable)
    except StopIteration:
        return None
    return first, itertools.chain([first], iterable)

def main(req: func.HttpRequest) -> func.HttpResponse:
    bodyJson = req.get_json()
    name = bodyJson.get("nom")
    group = bodyJson.get("groupe")
    days = bodyJson.get("days")

    ngValidation = validators.areNameGroupValid(name, group)
    if ngValidation != None:
        return func.HttpResponse(ngValidation, status_code=422)
    
    containerName="chiffres-lettres-games"
    blobConnString = os.environ['AzureWebJobsStorage']
    container_client = ContainerClient.from_connection_string(conn_str=blobConnString, container_name=containerName)
    scoreBlobs = []
    try:
        for i in range(0, days):
            strDate = (datetime.now() - timedelta(i)).strftime("%Y%m%d")
            prefix = f"{strDate}.{group}."
            blobs = container_client.list_blobs(prefix)
            for blob in blobs:
                scoreBlobs.append(blob)
    except:
        None

    if len(scoreBlobs) == 0:
        return func.HttpResponse(f"No scores available for group {group} in the last {days} days.")

    scores = []
    todayScores = []
    for blob in scoreBlobs:
        score = json.loads(container_client.download_blob(blob).content_as_text())
        scores.append(score)
        if blob.name.startswith(datetime.now().strftime("%Y%m%d")):
            todayScores.append(score)

    # Today's scores
    todayScoresSummary = []
    for s in todayScores:
        ps = {}
        ps["nom"] = s["joueur"]["nom"]
        ps["lettres"] = s["lettres"]["score"]
        ps["chiffres"] = s["chiffres"]["delta"]
        todayScoresSummary.append(ps)

    summary = {}
    for s in scores:
        nom = s["joueur"]["nom"]
        lettres = s["lettres"]["score"]
        chiffres = s["chiffres"]["delta"]
        if nom not in summary:
            summary[nom] = {}
            summary[nom]["lettres"] = lettres
            summary[nom]["chiffres"] = chiffres
            summary[nom]["parties"] = 1
        else:
            summary[nom]["lettres"] = summary[nom]["lettres"] + lettres
            summary[nom]["chiffres"] = summary[nom]["chiffres"] + chiffres
            summary[nom]["parties"] = summary[nom]["parties"] + 1
        

    res = {}
    res["today"] = todayScoresSummary
    res["history"] = summary

    return func.HttpResponse(json.dumps(res), mimetype="application/json")