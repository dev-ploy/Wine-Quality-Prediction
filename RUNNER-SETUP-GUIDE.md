# 🚀 GitHub Actions Self-Hosted Runner Setup Guide

This guide will help you set up a self-hosted GitHub Actions runner on your EC2 instance for automatic deployments.

---

## 📋 Prerequisites

- EC2 instance running Ubuntu
- SSH access to EC2
- GitHub repository access
- AWS credentials configured

---

## 🔧 Step 1: SSH into EC2

```bash
ssh -i "C:\Users\CHRISTY\Downloads\mlproject.pem" ubuntu@13.233.90.140
```

---

## 🔧 Step 2: Install Prerequisites

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y curl tar docker.io awscli

# Add ubuntu user to docker group
sudo usermod -aG docker ubuntu

# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Verify installations
docker --version
aws --version

# IMPORTANT: Logout and login again for docker group to take effect
exit
# SSH back in
```

---

## 🔧 Step 3: Configure AWS CLI

```bash
aws configure
```

When prompted, enter:
- **AWS Access Key ID**: [Your AWS Access Key]
- **AWS Secret Access Key**: [Your AWS Secret Key]
- **Default region name**: `ap-south-1`
- **Default output format**: `json`

Test AWS configuration:
```bash
aws ecr describe-repositories --region ap-south-1
```

---

## 🔧 Step 4: Download GitHub Actions Runner

```bash
# Create runner directory
mkdir -p ~/actions-runner && cd ~/actions-runner

# Download latest runner
curl -o actions-runner-linux-x64-2.311.0.tar.gz -L \
  https://github.com/actions/runner/releases/download/v2.311.0/actions-runner-linux-x64-2.311.0.tar.gz

# Extract
tar xzf ./actions-runner-linux-x64-2.311.0.tar.gz

# Clean up
rm actions-runner-linux-x64-2.311.0.tar.gz
```

---

## 🔧 Step 5: Get Runner Token from GitHub

1. Go to: `https://github.com/dev-ploy/Wine-Quality-Prediction/settings/actions/runners/new`
2. Select **Linux** as the operating system
3. Copy the **TOKEN** from the configuration command that looks like:
   ```
   ./config.sh --url https://github.com/dev-ploy/Wine-Quality-Prediction --token XXXXXXXXXXXXXXXXXXXXX
   ```

---

## 🔧 Step 6: Configure the Runner

```bash
cd ~/actions-runner

# Configure (replace YOUR_TOKEN with the token from GitHub)
./config.sh --url https://github.com/dev-ploy/Wine-Quality-Prediction --token YOUR_TOKEN

# When prompted:
# Enter name of runner: wine-quality-runner
# Enter runner group: [Press Enter for default]
# Enter labels: [Press Enter for default: self-hosted,Linux,X64]
# Enter work folder: [Press Enter for default: _work]
```

---

## 🔧 Step 7: Install Runner as a Service

```bash
# Install as systemd service
sudo ./svc.sh install

# Start the service
sudo ./svc.sh start

# Check status (should show "active (running)")
sudo ./svc.sh status

# Enable auto-start on boot
sudo systemctl enable actions.runner.dev-ploy-Wine-Quality-Prediction.wine-quality-runner.service
```

---

## 🔧 Step 8: Verify Runner Connection

1. Go to: `https://github.com/dev-ploy/Wine-Quality-Prediction/settings/actions/runners`
2. You should see your runner with a **green dot** (Idle status)

---

## 🎯 Step 9: Test the Pipeline

Trigger a deployment:
```bash
# On your local machine
git commit --allow-empty -m "Test automated deployment"
git push origin main
```

Or use GitHub web interface:
1. Go to: `https://github.com/dev-ploy/Wine-Quality-Prediction/actions`
2. Click "workflow" → "Run workflow" → "Run workflow"

---

## 📊 Monitoring

### Check Runner Status
```bash
sudo ./svc.sh status
```

### View Runner Logs
```bash
# Live logs
journalctl -u actions.runner.dev-ploy-Wine-Quality-Prediction.wine-quality-runner.service -f

# Recent logs
journalctl -u actions.runner.dev-ploy-Wine-Quality-Prediction.wine-quality-runner.service -n 100
```

### Check Docker Container
```bash
docker ps
docker logs wine-quality-app
```

---

## 🔄 Restart Runner

```bash
cd ~/actions-runner
sudo ./svc.sh stop
sudo ./svc.sh start
```

---

## 🆘 Troubleshooting

### Runner Not Appearing in GitHub
- Check if service is running: `sudo ./svc.sh status`
- Check logs: `journalctl -u actions.runner.* -n 50`
- Restart service: `sudo ./svc.sh stop && sudo ./svc.sh start`

### Docker Permission Denied
```bash
sudo usermod -aG docker ubuntu
# Logout and login again
```

### AWS CLI Not Working
```bash
aws configure
# Re-enter credentials
aws ecr describe-repositories --region ap-south-1
```

### Container Keeps Restarting
```bash
docker logs wine-quality-app
# Check for errors in the logs
```

---

## 🎉 Success Checklist

- [ ] EC2 instance accessible via SSH
- [ ] Docker installed and running
- [ ] AWS CLI configured with correct credentials
- [ ] GitHub Actions runner installed
- [ ] Runner service running and showing green in GitHub
- [ ] Test deployment successful
- [ ] Container running: `docker ps` shows wine-quality-app
- [ ] App accessible: `http://13.233.90.140:8080`
- [ ] Security Group allows port 8080 inbound

---

## 📝 Useful Commands

```bash
# Runner management
cd ~/actions-runner
sudo ./svc.sh status
sudo ./svc.sh stop
sudo ./svc.sh start
sudo ./svc.sh restart

# Docker management
docker ps                              # List running containers
docker logs wine-quality-app           # View container logs
docker logs -f wine-quality-app        # Follow logs
docker restart wine-quality-app        # Restart container
docker stop wine-quality-app           # Stop container
docker rm wine-quality-app             # Remove container

# AWS ECR
aws ecr get-login-password --region ap-south-1 | \
  docker login --username AWS --password-stdin \
  637423576642.dkr.ecr.ap-south-1.amazonaws.com

aws ecr describe-images --repository-name mlproj --region ap-south-1

# System monitoring
df -h                                  # Disk space
free -h                                # Memory
top                                    # Process monitor
```

---

## 🔐 Security Notes

- Keep your AWS credentials secure
- Regularly update the runner: `cd ~/actions-runner && ./config.sh remove && ./config.sh --url ... --token ...`
- Monitor runner logs for suspicious activity
- Use IAM roles with minimal permissions
- Enable CloudWatch monitoring

---

## 📚 References

- [GitHub Actions Self-Hosted Runners](https://docs.github.com/en/actions/hosting-your-own-runners)
- [AWS ECR Documentation](https://docs.aws.amazon.com/ecr/)
- [Docker Documentation](https://docs.docker.com/)
