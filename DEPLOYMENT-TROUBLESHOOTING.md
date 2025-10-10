# 🚨 EC2 Deployment Troubleshooting Guide

## Current Issue:
**ERR_CONNECTION_REFUSED** when accessing `http://13.233.90.140:8080`

---

## 🔧 STEP 1: Fix EC2 Security Group (CRITICAL!)

### AWS Console Method:
1. Go to **AWS Console** → **EC2** → **Instances**
2. Select your instance (13.233.90.140)
3. Go to **Security** tab
4. Click the **Security Group** name (e.g., sg-xxxxx)
5. Click **Edit inbound rules**
6. Click **Add rule**:
   ```
   Type: Custom TCP
   Port range: 8080
   Source: 0.0.0.0/0 (for testing)
   Description: Wine Quality App
   ```
7. Click **Save rules**

### AWS CLI Method:
```bash
# Get your security group ID
aws ec2 describe-instances --instance-ids <YOUR_INSTANCE_ID> --query 'Reservations[0].Instances[0].SecurityGroups[0].GroupId'

# Add port 8080 rule
aws ec2 authorize-security-group-ingress \
  --group-id <YOUR_SECURITY_GROUP_ID> \
  --protocol tcp \
  --port 8080 \
  --cidr 0.0.0.0/0
```

---

## 🔧 STEP 2: SSH into EC2 and Run Troubleshooting

### Connect to EC2:
```bash
ssh -i "your-key.pem" ubuntu@13.233.90.140
# Or if using ec2-user
ssh -i "your-key.pem" ec2-user@13.233.90.140
```

### Run Troubleshooting Script:
```bash
# Copy the script content or create it
nano troubleshoot.sh

# Paste the content from troubleshoot-deployment.sh
# Make it executable
chmod +x troubleshoot.sh

# Run it
./troubleshoot.sh
```

### Quick Manual Checks:
```bash
# Check if Docker is running
sudo systemctl status docker

# Check running containers
docker ps

# Check all containers
docker ps -a

# Check if port 8080 is listening
sudo netstat -tulpn | grep 8080

# Test locally
curl http://localhost:8080
```

---

## 🔧 STEP 3: Manual Deployment (If Container Not Running)

### Option A: Using the Script
```bash
# Create the deployment script
nano deploy.sh

# Paste the content from manual-deploy.sh
# Make it executable
chmod +x deploy.sh

# Run it
./deploy.sh
```

### Option B: Manual Commands
```bash
# 1. Login to ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  637423576642.dkr.ecr.ap-south-1.amazonaws.com

# 2. Pull the image
docker pull 637423576642.dkr.ecr.ap-south-1.amazonaws.com/mlproj:latest

# 3. Stop old container
docker stop wine-quality-app || true
docker rm wine-quality-app || true

# 4. Run new container
docker run -d \
  -p 8080:8080 \
  --name wine-quality-app \
  --restart unless-stopped \
  637423576642.dkr.ecr.ap-south-1.amazonaws.com/mlproj:latest

# 5. Check logs
docker logs -f wine-quality-app
```

---

## 🔧 STEP 4: Verify GitHub Actions Runner

```bash
# Check if runner is installed
ls -la /home/ubuntu/actions-runner/ || ls -la /opt/actions-runner/

# Check runner status
ps aux | grep actions-runner

# Check runner service (if using systemd)
sudo systemctl status actions.runner.*

# If runner is not running, start it
cd /home/ubuntu/actions-runner/  # or your runner path
./run.sh
```

---

## 🔧 STEP 5: Check GitHub Actions Logs

1. Go to: `https://github.com/dev-ploy/Wine-Quality-Prediction/actions`
2. Click on the latest workflow run
3. Check each job:
   - ✅ **integration** - Should pass
   - ✅ **build-and-push-ecr-image** - Should push image to ECR
   - ❓ **continuous-deployment** - Check for errors here

---

## 📋 Common Issues & Solutions

### Issue 1: Container Exits Immediately
**Symptom**: `docker ps` shows nothing, but `docker ps -a` shows exited container
**Solution**:
```bash
docker logs wine-quality-app  # Check the error
```
Common causes:
- Port already in use
- App crashes on startup
- Missing dependencies

### Issue 2: Port 8080 Already in Use
**Solution**:
```bash
# Find what's using port 8080
sudo lsof -i :8080
# Kill it
sudo kill -9 <PID>
# Or use a different port in the workflow
```

### Issue 3: AWS Credentials Not Set
**Solution**:
```bash
# Configure AWS CLI
aws configure
# Enter your credentials when prompted
```

### Issue 4: Image Not in ECR
**Solution**:
```bash
# Check if image exists
aws ecr describe-images --repository-name mlproj --region ap-south-1

# If not, trigger a new build by pushing to GitHub
```

---

## ✅ Success Checklist

- [ ] Security Group allows port 8080 inbound
- [ ] Docker is installed and running
- [ ] Container `wine-quality-app` is running (`docker ps`)
- [ ] Port 8080 is listening (`netstat -tulpn | grep 8080`)
- [ ] Local curl works: `curl http://localhost:8080`
- [ ] GitHub Actions deployment job succeeded
- [ ] Can access from browser: `http://13.233.90.140:8080`

---

## 🆘 Still Not Working?

**Share this information:**
1. Output of `docker ps -a`
2. Output of `docker logs wine-quality-app`
3. Output of `sudo netstat -tulpn | grep 8080`
4. Screenshot of GitHub Actions continuous-deployment job
5. EC2 Security Group inbound rules screenshot

---

## 🎯 Quick Test Commands

```bash
# All-in-one check
echo "Docker status:"; sudo systemctl status docker | grep Active
echo "Containers:"; docker ps
echo "Port 8080:"; sudo netstat -tulpn | grep 8080
echo "Local test:"; curl -I http://localhost:8080
```
