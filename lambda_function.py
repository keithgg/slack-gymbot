import json
from gymbot import send_exercise_message


def lambda_handler(event, context):
    send_exercise_message()
    return {"statusCode": 200, "body": json.dumps("done")}
