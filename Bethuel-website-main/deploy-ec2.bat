@echo off
echo 🚀 Deploying Bethuel Portfolio to AWS EC2...

REM Configuration
set KEY_NAME=bethuel-portfolio-key
set SECURITY_GROUP=bethuel-portfolio-sg
set INSTANCE_TYPE=t3.micro

REM Ubuntu 22.04 LTS AMI for eu-west-1
set AMI_ID=ami-0905a3c97561e0b69

REM Create security group if it doesn't exist
echo 🔒 Setting up security group...
aws ec2 create-security-group --group-name %SECURITY_GROUP% --description "Security group for Bethuel Portfolio" >nul 2>&1

REM Add security group rules
aws ec2 authorize-security-group-ingress --group-name %SECURITY_GROUP% --protocol tcp --port 22 --cidr 0.0.0.0/0 >nul 2>&1
aws ec2 authorize-security-group-ingress --group-name %SECURITY_GROUP% --protocol tcp --port 80 --cidr 0.0.0.0/0 >nul 2>&1
aws ec2 authorize-security-group-ingress --group-name %SECURITY_GROUP% --protocol tcp --port 8080 --cidr 0.0.0.0/0 >nul 2>&1

REM Launch EC2 instance
echo 🖥️ Launching EC2 instance...
for /f "tokens=*" %%i in ('aws ec2 run-instances --image-id %AMI_ID% --count 1 --instance-type %INSTANCE_TYPE% --key-name %KEY_NAME% --security-groups %SECURITY_GROUP% --user-data fileb://aws/ec2-user-data.sh --query "Instances[0].InstanceId" --output text') do set INSTANCE_ID=%%i

if not "%INSTANCE_ID%"=="" (
    echo ✅ Instance launched: %INSTANCE_ID%
    
    REM Wait for instance to be running
    echo ⏳ Waiting for instance to be running...
    aws ec2 wait instance-running --instance-ids %INSTANCE_ID%
    
    REM Get public IP
    for /f "tokens=*" %%i in ('aws ec2 describe-instances --instance-ids %INSTANCE_ID% --query "Reservations[0].Instances[0].PublicIpAddress" --output text') do set PUBLIC_IP=%%i
    
    echo 🌐 Instance is running!
    echo 📍 Public IP: %PUBLIC_IP%
    echo 🔗 SSH: ssh -i %KEY_NAME%.pem ubuntu@%PUBLIC_IP%
    echo 🌍 Website: http://%PUBLIC_IP%:8080
    echo.
    echo ⏳ Please wait 5-10 minutes for the application to fully deploy...
) else (
    echo ❌ Failed to launch instance
    exit /b 1
)

pause