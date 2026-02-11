import json
import os
import time
import uuid
from decimal import Decimal
import boto3

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = os.environ["TABLE_NAME"]
table = dynamodb.Table(TABLE_NAME)

def _json_default(o):
    # DynamoDB returns numbers as Decimal
    if isinstance(o, Decimal):
        # timestamps & integer-like values
        if o % 1 == 0:
            return int(o)
        return float(o)
    raise TypeError(f"Object of type {o.__class__.__name__} is not JSON serializable")

def _response(status_code: int, body: dict):
    return {
        "statusCode": status_code,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body, default=_json_default),
    }

def handler(event, context):
    method = event.get("requestContext", {}).get("http", {}).get("method", "")
    path = event.get("rawPath", "")

    # POST /message
    if method == "POST" and path == "/message":
        body_str = event.get("body") or "{}"
        try:
            payload = json.loads(body_str)
        except json.JSONDecodeError:
            return _response(400, {"error": "Invalid JSON body"})

        name = (payload.get("name") or "").strip()
        message = (payload.get("message") or "").strip()

        if not name or not message:
            return _response(400, {"error": "Both 'name' and 'message' are required"})

        item_id = str(uuid.uuid4())
        ts = int(time.time())

        table.put_item(Item={
            "id": item_id,
            "name": name,
            "message": message,
            "timestamp": ts
        })

        return _response(201, {"id": item_id, "stored": True})

    # GET /message/{id}
    if method == "GET" and path.startswith("/message/"):
        item_id = path.split("/message/")[1].strip()
        if not item_id:
            return _response(400, {"error": "Missing id"})

        res = table.get_item(Key={"id": item_id})
        item = res.get("Item")
        if not item:
            return _response(404, {"error": "Not found", "id": item_id})

        return _response(200, item)

    return _response(404, {"error": "Route not found", "method": method, "path": path})
