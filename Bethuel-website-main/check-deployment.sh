#!/bin/bash

INSTANCE_ID="i-0476a1c47861241cd"
ELASTIC_IP="34.252.250.140"

echo "🔍 Checking EC2 instance status..."
aws ec2 describe-instances --instance-ids $INSTANCE_ID --query 'Reservations[0].Instances[0].State.Name' --output text

echo "🔍 Checking security group rules..."
aws ec2 describe-security-groups --group-names bethuel-portfolio-sg --query 'SecurityGroups[0].IpPermissions'

echo "🔍 Testing SSH connection..."
ssh -i bethuel-portfolio-key.pem -o ConnectTimeout=10 ubuntu@$ELASTIC_IP "echo 'SSH works'"

echo "🔍 Checking Docker containers..."
ssh -i bethuel-portfolio-key.pem ubuntu@$ELASTIC_IP "sudo docker ps"

echo "🔍 Checking nginx logs..."
ssh -i bethuel-portfolio-key.pem ubuntu@$ELASTIC_IP "sudo docker logs bethuelportfoliowebsite_nginx_1 --tail 20"

echo "🔍 Testing port 8080..."
curl -I http://$ELASTIC_IP:8080 --connect-timeout 10