import json
import azure.functions as func
from shared_code import hand

def main(req: func.HttpRequest) -> func.HttpResponse:
    group = req.params.get('group')
    return func.HttpResponse(json.dumps(hand.hand(group)), mimetype="application/json")