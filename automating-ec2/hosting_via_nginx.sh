#!/bin/bash

sudo apt-get update -y

sudo apt-get install nginx -y

echo "Hello everyone, my IP address is $(hostname -i)" | sudo tee /var/www/html/index.html

sudo systemctl restart nginx
