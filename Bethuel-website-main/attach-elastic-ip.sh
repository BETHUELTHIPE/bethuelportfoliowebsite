#!/bin/bash

INSTANCE_ID="i-0476a1c47861241cd"

echo "🔗 Creating Elastic IP..."
ALLOCATION_ID=$(aws ec2 allocate-address --domain vpc --query 'AllocationId' --output text)

echo "📌 Attaching Elastic IP to instance..."
aws ec2 associate-address --instance-id $INSTANCE_ID --allocation-id $ALLOCATION_ID

ELASTIC_IP=$(aws ec2 describe-addresses --allocation-ids $ALLOCATION_ID --query 'Addresses[0].PublicIp' --output text)

echo "✅ Elastic IP attached!"
echo "🌐 Static IP: $ELASTIC_IP"
echo "🔗 SSH: ssh -i bethuel-portfolio-key.pem ubuntu@$ELASTIC_IP"
echo "🌍 Website: http://$ELASTIC_IP:8080"