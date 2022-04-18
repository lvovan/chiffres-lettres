import re
import logging
import json
from py_expression_eval import Parser
from shared_code import hand
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    bodyJson = req.get_json()
    name = bodyJson.get("name")
    formula = bodyJson.get("formula")
    h = hand.hand()
    # Check if formula contains bag numbers
    # logging.info(formula)
    numbersInHand = h["chiffres"]["l"]
    matches = re.finditer(r"(\d+)", formula)
    numbersUsed = 0
    for match in matches:
        number = int(match.group())
        if number not in numbersInHand:
            return func.HttpResponse(f"Invalid move: {number} not in hand {numbersInHand}.", status_code=400)
        numbersInHand.remove(number)
        numbersUsed += 1
        # logging.info(f" > {numbersInHand}")

    parser = Parser()
    f = parser.parse(formula)

    targetNumber = int(h["chiffres"]["n"])
    res = {}
    res["name"] = name
    res["delta"] = abs(int(h["chiffres"]["n"]) - f.evaluate({}))
    res["numbersUsed"] = numbersUsed

    return func.HttpResponse(json.dumps(res), mimetype="application/json")
