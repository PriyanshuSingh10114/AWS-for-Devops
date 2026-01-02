<h1>EC2-to-RDS</h1>

<h2>Step 1: Create RDS MySQL Instance</h2>

Go to RDS → Create database

Choose:

Engine: MySQL

Template: Free tier

Configure:

DB instance identifier: my-rds-db

Master username: admin

Password: set a strong password

Connectivity:

VPC: same as EC2

Public access: No

VPC security group: create new (or existing)

Database port: 3306

Create database

Wait until status becomes Available.

---

<h2>Step 2: Configure RDS Security Group</h2>

Edit Inbound rules of RDS security group:

Type	Protocol	Port	Source
MySQL/Aurora	TCP	3306	EC2 Security Group

This ensures only EC2 can access RDS.

---

<h2>Step 3: Create IAM Role for EC2</h2>

Go to IAM → Roles → Create role

Trusted entity: AWS service

Use case: EC2

Attach policies:

AmazonRDSFullAccess

CloudWatchFullAccess

Role name: ec2-rds-cloudwatch-role

Create role

---

</h2>Step 4: Launch EC2 Instance</h2>

Go to EC2 → Launch instance

Choose:

AMI: Ubuntu 22.04

Instance type: t2.micro

Key pair: select existing

Network:

Same VPC as RDS

Public subnet

Security group (EC2):

Allow SSH (22) from your IP

IAM Role:

Attach ec2-rds-cloudwatch-role

Launch instance

---

</h2>Step 5: Connect to EC2</h2>

    ssh -i your-key.pem ubuntu@<EC2_PUBLIC_IP>

Update System Packages

    sudo apt update
    sudo apt upgrade -y

Install MySQL Client

    sudo apt install mysql-client -y


Verify installation:

    mysql --version

---

</h2>Step 6: Get RDS Endpoint (DNS)</h2>

Go to RDS → Databases

Select your DB

Copy Endpoint

    my-rds-db.xxxxx.ap-south-1.rds.amazonaws.com

---

</h2>Step 7: Connect EC2 to RDS MySQL</h2>

    mysql -h <RDS_ENDPOINT> -u admin -p -P 3306


    Enter the RDS password.

If connected successfully, you are now inside RDS MySQL, not EC2.

---

<h2>Step 8: Create Database</h2>

    CREATE DATABASE company;
    USE company;
    
    Step 11: Create Table
    CREATE TABLE employees (
        id INT PRIMARY KEY,
        name VARCHAR(50),
        role VARCHAR(50)
    );

Insert Data

    INSERT INTO employees VALUES (1, 'Priyanshu', 'DevOps Engineer');
    INSERT INTO employees VALUES (2, 'Aman', 'Backend Developer');

<h2>Step 9: Verify Data</h2>

    SELECT * FROM employees;
    
    
    Expected output:
    
    +----+-----------+-------------------+
    | id | name      | role              |
    +----+-----------+-------------------+
    |  1 | Priyanshu | DevOps Engineer   |
    |  2 | Aman      | Backend Developer |
    +----+-----------+-------------------+

Step 14: Observe Changes in RDS Console

Go to RDS → Query Editor (optional)
OR Use any SQL client (MySQL Workbench, DBeaver)

AWS RDS Console does NOT show table rows directly
Data must be viewed via SQL queries only.
