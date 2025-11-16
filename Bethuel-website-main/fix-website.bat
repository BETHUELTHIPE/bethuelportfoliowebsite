@echo off
set INSTANCE_ID=i-0476a1c47861241cd
set ELASTIC_IP=34.252.250.140

echo 🔍 Step 1: Checking instance status...
aws ec2 describe-instances --instance-ids %INSTANCE_ID% --query "Reservations[0].Instances[0].State.Name" --output text

echo.
echo 🔍 Step 2: Testing SSH connection...
ssh -i bethuel-portfolio-key.pem -o ConnectTimeout=10 ubuntu@%ELASTIC_IP% "echo SSH works"

echo.
echo 🔍 Step 3: Checking Docker containers...
ssh -i bethuel-portfolio-key.pem ubuntu@%ELASTIC_IP% "sudo docker ps"

echo.
echo 🔍 Step 4: Starting Docker services if needed...
ssh -i bethuel-portfolio-key.pem ubuntu@%ELASTIC_IP% "cd bethuelportfoliowebsite && sudo docker-compose up -d"

echo.
echo 🔍 Step 5: Testing website...
curl -I http://%ELASTIC_IP%:8080 --connect-timeout 10

pause