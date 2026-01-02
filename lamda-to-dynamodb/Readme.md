<h1>Lambda-dynamodb setup</h1>

<h2>Step 1: Create DynamoDB Table</h2>

Open AWS Console → DynamoDB

Click Create table

Configure:

Table name: learners

Partition key:

Name: learner_id

Type: String

Keep default settings

Click Create table

Wait until table status is Active.

---

<h2>Step 2: Create IAM Role for Lambda</h2>

Open IAM → Roles

Click Create role

Select Trusted entity:

AWS service

Use case: Lambda

Click Next

Attach Permissions

Attach the following policies:

AWSDynamoDBFullAccess
AWSCloudWatchFullAccess

You will see a policy on your screen after continuing


Name the role: lambda-dynamodb-role

Create role

---

<h2>Step 3: Create Lambda Function</h2>

Open AWS Console → Lambda

Click Create function

Choose:

Author from scratch

Function name: insert-to-dynamo

Runtime: Python 3.12

Execution role: Use existing role

Role: lambda-dynamodb-role

Click Create function

---

<h2>Step 4: Lambda Code – Insert Item into DynamoDB</h2>

Replace the default Lambda code with:

    import json
    import boto3
    
    def lambda_handler(event, context):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("learners")

        table.put_item(
            Item={
                "learner_id": "2",
                "name": "Priyanshu",
                "course": "AWS",
                "status": "active"
            }
        )
    
        return {
            "statusCode": 200,
            "body": json.dumps("Item inserted successfully")
        }


Click Deploy.

---

<h2>Step 5: Test Insert Operation</h2>

Click Test

Create a test event:

    {
      "message": "insert-event"
    }


Run test

Expected Result

Status: Succeeded

Message: "Item inserted successfully"

---

<h2>Step 6: Verify Insert in DynamoDB</h2>

Open DynamoDB → Tables → learners

Click Explore table items

You should see:

    learner_id = 2

name, course, status fields

---

<h2>Step 7: Lambda Code – Delete Item from DynamoDB</h2>

Update Lambda code to:

    import json
    import boto3
    
    def lambda_handler(event, context):
        dynamodb = boto3.resource("dynamodb")
        table = dynamodb.Table("learners")

        table.delete_item(
            Key={
                "learner_id": "2"
            }
        )
    
        return {
            "statusCode": 200,
            "body": json.dumps("Item deleted successfully")
        }


Click Deploy.

---

<h2>Step 8: Test Delete Operation</h2>

Run the same test event

Lambda execution should succeed

---

<h2>Step 9: Verify Deletion in DynamoDB</h2>

Open DynamoDB → learners

Explore table items

Item with learner_id = 2 should no longer exist

---

<h3>Important Notes</h3>

DynamoDB Behavior

put_item() overwrites existing items with same key

delete_item() does NOT throw error if item does not exist

Lambda success does not always mean business logic success

---

