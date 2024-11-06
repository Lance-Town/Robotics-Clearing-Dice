import json

def genJSON(type: str, dicePosition: list) -> str:
    responseData = {
        "type": type,
        "dicePosition": dicePosition,
    }

    return json.dumps(responseData)