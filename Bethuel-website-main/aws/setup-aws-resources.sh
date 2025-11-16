#!/bin/bash

# Setup AWS Resources for Bethuel Portfolio
set -e

AWS_REGION="us-east-1"
echo "🔧 Setting up AWS resources..."

# Step 1: Create IAM role for ECS task execution
echo "👤 Creating ECS task execution role..."
aws iam create-role \
    --role-name ecsTaskExecutionRole \
    --assume-role-policy-document file://aws/task-execution-trust.json

aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# Step 2: Create secrets in AWS Secrets Manager
echo "🔐 Creating secrets in AWS Secrets Manager..."
aws secretsmanager create-secret \
    --name "bethuel-portfolio-secrets" \
    --description "Secrets for Bethuel Portfolio application" \
    --secret-string file://aws/secrets.json \
    --region $AWS_REGION

# Step 3: Create VPC and networking (if needed)
echo "🌐 Setting up VPC..."
VPC_ID=$(aws ec2 create-vpc \
    --cidr-block 10.0.0.0/16 \
    --query 'Vpc.VpcId' \
    --output text \
    --region $AWS_REGION)

echo "VPC ID: $VPC_ID"

# Create subnet
SUBNET_ID=$(aws ec2 create-subnet \
    --vpc-id $VPC_ID \
    --cidr-block 10.0.1.0/24 \
    --availability-zone ${AWS_REGION}a \
    --query 'Subnet.SubnetId' \
    --output text \
    --region $AWS_REGION)

echo "Subnet ID: $SUBNET_ID"

# Create internet gateway
IGW_ID=$(aws ec2 create-internet-gateway \
    --query 'InternetGateway.InternetGatewayId' \
    --output text \
    --region $AWS_REGION)

aws ec2 attach-internet-gateway \
    --vpc-id $VPC_ID \
    --internet-gateway-id $IGW_ID \
    --region $AWS_REGION

# Create security group
SG_ID=$(aws ec2 create-security-group \
    --group-name bethuel-portfolio-sg \
    --description "Security group for Bethuel Portfolio" \
    --vpc-id $VPC_ID \
    --query 'GroupId' \
    --output text \
    --region $AWS_REGION)

# Allow HTTP traffic
aws ec2 authorize-security-group-ingress \
    --group-id $SG_ID \
    --protocol tcp \
    --port 8000 \
    --cidr 0.0.0.0/0 \
    --region $AWS_REGION

echo "✅ AWS resources created successfully!"
echo "📝 Update your task definition with:"
echo "   Subnet ID: $SUBNET_ID"
echo "   Security Group ID: $SG_ID"
echo ""
echo "🚀 Next steps:"
echo "1. Update aws/secrets.json with your actual secrets"
echo "2. Run: aws secretsmanager update-secret --secret-id bethuel-portfolio-secrets --secret-string file://aws/secrets.json"
echo "3. Update subnet and security group IDs in deploy-to-aws.sh"
echo "4. Run: ./aws/deploy-to-aws.sh"