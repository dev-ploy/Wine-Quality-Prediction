# EC2 Debugging Guide

## SSH into your EC2 instance:
```bash
ssh -i "your-key.pem" ubuntu@13.233.90.140
```

## Check if Docker container is running:
```bash
docker ps
```
Expected output: Should show `wine-quality-app` container running on port 8080

## If container is not running, check logs:
```bash
docker ps -a  # Show all containers including stopped ones
docker logs wine-quality-app  # Check container logs
```

## Check if port 8080 is listening:
```bash
sudo netstat -tulpn | grep 8080
# OR
sudo ss -tulpn | grep 8080
```

## Test locally on EC2:
```bash
curl http://localhost:8080
```
If this works, it's a security group issue. If not, the app isn't running.

## Manually pull and run the container (if needed):
```bash
# Login to ECR
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 637423576642.dkr.ecr.ap-south-1.amazonaws.com

# Pull the image
docker pull 637423576642.dkr.ecr.ap-south-1.amazonaws.com/mlproj:latest

# Stop old container
docker stop wine-quality-app || true
docker rm wine-quality-app || true

# Run new container
docker run -d -p 8080:8080 --name wine-quality-app 637423576642.dkr.ecr.ap-south-1.amazonaws.com/mlproj:latest

# Check logs
docker logs -f wine-quality-app
```

## Check GitHub Actions runner:
```bash
# Check if runner is active
ps aux | grep actions-runner
sudo systemctl status actions.runner.*
```
