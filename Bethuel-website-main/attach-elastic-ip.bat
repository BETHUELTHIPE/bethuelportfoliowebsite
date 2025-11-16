@echo off
set INSTANCE_ID=i-0476a1c47861241cd

echo 🔗 Creating Elastic IP...
for /f "tokens=*" %%i in ('aws ec2 allocate-address --domain vpc --query "AllocationId" --output text') do set ALLOCATION_ID=%%i

echo 📌 Attaching Elastic IP to instance...
aws ec2 associate-address --instance-id %INSTANCE_ID% --allocation-id %ALLOCATION_ID%

for /f "tokens=*" %%i in ('aws ec2 describe-addresses --allocation-ids %ALLOCATION_ID% --query "Addresses[0].PublicIp" --output text') do set ELASTIC_IP=%%i

echo ✅ Elastic IP attached!
echo 🌐 Static IP: %ELASTIC_IP%
echo 🔗 SSH: ssh -i bethuel-portfolio-key.pem ubuntu@%ELASTIC_IP%
echo 🌍 Website: http://%ELASTIC_IP%:8080

pause