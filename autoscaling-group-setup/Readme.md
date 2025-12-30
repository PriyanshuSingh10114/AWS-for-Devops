<h1>Autoscaling setup</h1>

Prerequisites (What you already have)

You already mentioned:

Launch Template created

Website setup via User Data script (Nginx / Apache)

Ports 22, 80, 443 allowed

Instance type: t2.micro

OS: Ubuntu

---

Verify Your Launch Template (Very Important)

Go to:
EC2 → Launch Templates → Your Template

Check once:

Setting	Must Be

    AMI	Ubuntu
    Instance Type	t2.micro
    Security Group	Allows 80, 443, 22
    User Data	Installs & starts web server
    Key Pair	

---


Example (correct):

#!/bin/bash
apt update -y
apt install nginx -y
echo "Hello from $(hostname -I)" > /var/www/html/index.html
systemctl restart nginx

---

Create Target Group (For Load Balancer)

Auto Scaling must be attached to a Target Group.

Steps:

EC2 → Target Groups → Create

Type: Instances

Protocol: HTTP

Port: 80

VPC: Same as EC2

Health Check:

Path: /

Healthy threshold: 2

Interval: 30s

Do NOT register instances manually
ASG will handle this automatically.

---

Create Application Load Balancer (ALB)
Steps:

EC2 → Load Balancers → Create

Choose Application Load Balancer

Internet-facing

Listener:

HTTP : 80

Select:

At least 2 public subnets (mandatory)

Security Group:

Allow HTTP 80 from 0.0.0.0/0

Attach Target Group (from step 2)

Once created, copy the ALB DNS name
(example: my-alb-123.ap-south-1.elb.amazonaws.com)

---

Create Auto Scaling Group (Using Your Launch Template)
Steps:

EC2 → Auto Scaling Groups → Create

Name: web-asg

Launch Template:

Select your existing template

Version: Latest

---

Configure Networking for ASG

Select same VPC

Choose multiple subnets (for HA)

Attach Load Balancer

Choose Application Load Balancer

Select the Target Group


Traffic → ALB → EC2 instances

No direct public access required

---

Set Desired, Min & Max Capacity

Recommended (start small):

Setting	Value
Desired	1
Minimum	1
Maximum	4

💡 You pay only for running instances

---

Configure Auto Scaling Policy (CPU > 20%)
Choose:

👉 Target Tracking Scaling Policy

Settings:

Metric: Average CPU Utilization

Target value: 20

Cooldown: Default

This means:

CPU > 20% → New instance launches

CPU < 20% → Instance terminates automatically

Behind the scenes, this uses Amazon CloudWatch metrics.

---

Health Checks (Critical)

Set:

Health Check Type: ELB

Grace Period: 300 seconds

Why?

Allows EC2 time to install packages via User Data

Prevents premature termination

---

Create Auto Scaling Group

Click Create ASG

Within 2–3 minutes:

EC2 instance launches

Registers with ALB

Website becomes live

---

Access Your Website

Use:

http://<ALB-DNS-NAME>


✔️ Never use EC2 public IP
✔️ ALB handles traffic + scaling

---

Test Auto Scaling (Real Validation)

SSH into one instance and run:

sudo apt install stress -y
stress --cpu 2 --timeout 300


Observe:

CPU > 20%

ASG launches new EC2

Target Group shows 2 healthy instances
