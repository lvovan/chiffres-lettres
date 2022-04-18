import logging
import json
from shared_code import solver
import azure.functions as func
import pydawg
import pathlib

def main(req: func.HttpRequest) -> func.HttpResponse:
    res = solver.solver()
    return func.HttpResponse(json.dumps(res), mimetype="application/json")