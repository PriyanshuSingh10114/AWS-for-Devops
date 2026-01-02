import json
import boto3

def lambda_handler(event, context):
    print(event["message"])

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("learners")

    response = table.delete_item(
        Key={
            "learner_id": "1"   
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Item deleted successfully from DynamoDB")
    }
