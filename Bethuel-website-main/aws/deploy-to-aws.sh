#!/bin/bash

# AWS ECS Deployment Script for Bethuel Portfolio
set -e

# Configuration
AWS_REGION="us-east-1"
CLUSTER_NAME="bethuel-portfolio-cluster"
SERVICE_NAME="bethuel-portfolio-service"
TASK_FAMILY="bethuel-portfolio-task"
ECR_REPO="bethuel-portfolio"

echo "🚀 Deploying Bethuel Portfolio to AWS ECS..."

# Get AWS Account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Account ID: $ACCOUNT_ID"

# Step 1: Create ECR Repository
echo "📦 Creating ECR repository..."
aws ecr create-repository --repository-name $ECR_REPO --region $AWS_REGION || echo "Repository already exists"

# Step 2: Build and push Docker image
echo "🔨 Building and pushing Docker image..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker build -t $ECR_REPO .
docker tag $ECR_REPO:latest $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest
docker push $ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$ECR_REPO:latest

# Step 3: Create ECS Cluster
echo "🏗️ Creating ECS cluster..."
aws ecs create-cluster --cluster-name $CLUSTER_NAME --region $AWS_REGION || echo "Cluster already exists"

# Step 4: Create CloudWatch Log Group
echo "📊 Creating CloudWatch log group..."
aws logs create-log-group --log-group-name "/ecs/bethuel-portfolio" --region $AWS_REGION || echo "Log group already exists"

# Step 5: Attach policy to execution role
echo "🔐 Attaching policies to execution role..."
aws iam attach-role-policy \
    --role-name ecsTaskExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# Step 6: Update task definition with account ID
echo "📝 Updating task definition..."
sed "s/YOUR_ACCOUNT_ID/$ACCOUNT_ID/g" aws/ecs-task-definition.json > aws/ecs-task-definition-updated.json

# Step 7: Register task definition
echo "📋 Registering task definition..."
aws ecs register-task-definition \
    --cli-input-json file://aws/ecs-task-definition-updated.json \
    --region $AWS_REGION

# Step 8: Create or update service
echo "🌐 Creating ECS service..."
aws ecs create-service \
    --cluster $CLUSTER_NAME \
    --service-name $SERVICE_NAME \
    --task-definition $TASK_FAMILY \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678],securityGroups=[sg-12345678],assignPublicIp=ENABLED}" \
    --region $AWS_REGION || echo "Service already exists, updating..."

# If service exists, update it
aws ecs update-service \
    --cluster $CLUSTER_NAME \
    --service $SERVICE_NAME \
    --task-definition $TASK_FAMILY \
    --region $AWS_REGION || echo "Service updated"

echo "✅ Deployment complete!"
echo "🌐 Your portfolio will be available at the ECS service endpoint"
echo "📊 Monitor logs: aws logs tail /ecs/bethuel-portfolio --follow"