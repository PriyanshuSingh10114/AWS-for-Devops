import json
import boto3

def lambda_handler(event, context):
    print(event["message"])

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("learners")

    response = table.put_item(
        Item={
            "learner_id": "1",        
            "name": "Priyanshu",
            "course": "AWS",
            "status": "active"
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps("Data inserted successfully into DynamoDB")
    }

