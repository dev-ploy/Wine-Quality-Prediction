#!/bin/bash

echo "=========================================="
echo "Wine Quality App Deployment Troubleshooting"
echo "=========================================="
echo ""

echo "1. Checking if Docker is installed and running..."
docker --version
sudo systemctl status docker | grep Active
echo ""

echo "2. Checking running Docker containers..."
docker ps
echo ""

echo "3. Checking ALL Docker containers (including stopped)..."
docker ps -a
echo ""

echo "4. Checking if port 8080 is listening..."
sudo netstat -tulpn | grep 8080 || echo "Port 8080 is NOT listening"
echo ""

echo "5. Checking GitHub Actions runner status..."
ps aux | grep actions-runner | grep -v grep || echo "Runner not found in processes"
echo ""

echo "6. Checking wine-quality-app container logs (if exists)..."
if docker ps -a | grep -q wine-quality-app; then
    echo "Container exists. Last 50 lines of logs:"
    docker logs --tail 50 wine-quality-app
else
    echo "wine-quality-app container does NOT exist"
fi
echo ""

echo "7. Checking disk space..."
df -h
echo ""

echo "8. Checking if we can reach ECR..."
aws ecr describe-repositories --repository-names mlproj --region ap-south-1 2>&1 || echo "Cannot access ECR"
echo ""

echo "9. Testing local connectivity..."
curl -I http://localhost:8080 2>&1 || echo "Cannot connect to localhost:8080"
echo ""

echo "=========================================="
echo "Troubleshooting Complete!"
echo "=========================================="
