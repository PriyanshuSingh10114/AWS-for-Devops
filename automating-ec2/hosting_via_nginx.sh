#!/bin/bash

sudo apt-get update -y

sudo apt-get install nginx -y

echo "Hello everyone, my IP address is $(hostname -i)" | sudo tee /var/www/html/index.html

sudo systemctl restart nginx


#add this script in advanced section at the end in the code section and then launch instance
#after launching take ip of ec2 instance and port 80 default port for nginx serverr make sure you have provided outbound access to that 
#then http://<ec2-ip-address>:80  run this in your browser
