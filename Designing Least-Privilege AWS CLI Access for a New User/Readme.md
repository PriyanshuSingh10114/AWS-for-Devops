<h1>Secure AWS Onboarding for User (EC2 + S3 via CLI Only)</h1>

When a new user joins an engineering team, the common instinct is to give full AWS Console access so they can “learn faster.”
In production environments, this shortcut introduces unnecessary risk.

---
This repository documents a real-world onboarding pattern where a fresher is:


    - Allowed to use AWS CLI only
    
    - Restricted to EC2 instance operations
    
    - Allowed read-only access to a specific S3 bucket
    
    - Blocked from IAM, networking, databases, billing, and other services

---

Architecture Overview

Flow:

    Admin (Root user) creates IAM user and policies via AWS Console
    
    Admin generates Access Key + Secret Key
    
    Fresher configures AWS CLI locally
    
    Fresher interacts only with EC2 and S3 (read-only)
    
    All other AWS services are blocked by default

Prerequisites

    AWS account with root or admin access
    
    AWS CLI installed on fresher’s system
    
    Target AWS region (example used: ap-south-1)
    
    Step 1: Create IAM User (Admin Side)
    
    Go to IAM → Users → Create user

Username:

    fresher-ec2-s3-cli

    Do NOT enable AWS Console access

Step 2: Create EC2 Limited Access Policy

Create a customer-managed policy named:

    EC2LimitedAccessPolicy

Step 3: Create S3 Read-Only Policy (Scoped to One Bucket)

Create a policy named:

    S3ReadOnlySpecificBucket

Step 4: Attach Policies to the User

Attach both policies to the IAM user:

    EC2LimitedAccessPolicy
    
    S3ReadOnlySpecificBucket

At this point, permissions are fully constrained.

Step 5: Generate Access Keys

    Open the IAM user
    
    Go to Security Credentials

    Create Access Key

Select:

    Command Line Interface (CLI)


Securely share with the fresher:

    Access Key ID
    
    Secret Access Key


Step 6: User Setup – Install AWS CLI

Verify Installation

    aws --version

Install (Ubuntu)

    sudo apt update && sudo apt install awscli -y

Step 7: Configure AWS CLI (Fresher Side)

    aws configure


Provide:

    AWS Access Key ID:     <ACCESS_KEY>
    AWS Secret Access Key: <SECRET_KEY>
    Default region name:  ap-south-1
    Default output format: json

Allowed Commands 

    aws ec2 describe-instances
    aws ec2 stop-instances --instance-ids i-xxxxxxxx
    aws s3 ls s3://example-bucket-name
    aws s3 cp s3://example-bucket-name/file.txt .

Why This Approach Is Production-Safe

    No console access → no accidental clicks
    
    Service-level IAM policies → minimal blast radius
    
    CLI-only workflow → mirrors real DevOps practices
    
    Easy revocation → delete access key instantly
    
    This is how mature teams onboard juniors without compromising security.

To revoke access immediately:
    
    IAM → User → Security Credentials → Deactivate/Delete Access Key


Or delete the user entirely if no longer needed.

This setup enables User to work confidently while protecting production infrastructure.
