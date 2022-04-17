import json
import azure.functions as func
from shared_code import hand

def main(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(json.dumps(hand.hand()), mimetype="application/json")