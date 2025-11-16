@echo off
set INSTANCE_ID=i-0476a1c47861241cd

echo 🛑 Stopping EC2 instance...
aws ec2 stop-instances --instance-ids %INSTANCE_ID%

echo ⏳ Waiting for instance to stop...
aws ec2 wait instance-stopped --instance-ids %INSTANCE_ID%

echo 🔧 Upgrading to t3.large...
aws ec2 modify-instance-attribute --instance-id %INSTANCE_ID% --instance-type Value=t3.large

echo 🚀 Starting instance...
aws ec2 start-instances --instance-ids %INSTANCE_ID%

echo ⏳ Waiting for instance to start...
aws ec2 wait instance-running --instance-ids %INSTANCE_ID%

echo ✅ Instance upgraded to t3.large!
echo 🌐 Your website: http://34.252.250.140:8080

pause