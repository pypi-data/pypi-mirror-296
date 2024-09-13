import json

event_arns = ["arn:cron"]


def reduce_event_source(event: dict) -> str:
    mapping: dict = event.get("mapping")
    fields = []
    for key, val in mapping.items():
        if isinstance(val, dict):
            val = "'{}'".format(json.dumps(val))
        fields.append("{}={}".format(key, val))
    return "Endpoints={"+",".join(fields)+"}"


def reduce_url_cors(cors: dict) -> str:
    fields = []
    for key, val in cors.items():
        key = key[0].upper() + key[1:]
        fields.append("{}={}".format(key, val))
    return ",".join(fields)
