#!/bin/bash

echo "=========================================="
echo "Manual Deployment of Wine Quality App"
echo "=========================================="
echo ""

# Set variables
ECR_REGISTRY="637423576642.dkr.ecr.ap-south-1.amazonaws.com"
ECR_REPOSITORY="mlproj"
IMAGE_TAG="latest"
CONTAINER_NAME="wine-quality-app"
PORT="8080"

echo "Step 1: Login to Amazon ECR..."
aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to login to ECR. Check AWS credentials."
    exit 1
fi
echo "✓ Successfully logged in to ECR"
echo ""

echo "Step 2: Pulling latest image from ECR..."
docker pull $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to pull image. Check if image exists in ECR."
    exit 1
fi
echo "✓ Successfully pulled image"
echo ""

echo "Step 3: Stopping and removing old container..."
docker stop $CONTAINER_NAME 2>/dev/null || true
docker rm $CONTAINER_NAME 2>/dev/null || true
echo "✓ Old container removed"
echo ""

echo "Step 4: Running new container..."
docker run -d \
    -p $PORT:$PORT \
    --name $CONTAINER_NAME \
    --restart unless-stopped \
    $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG

if [ $? -ne 0 ]; then
    echo "ERROR: Failed to start container"
    exit 1
fi
echo "✓ Container started successfully"
echo ""

echo "Step 5: Checking container status..."
sleep 3
docker ps | grep $CONTAINER_NAME

echo ""
echo "Step 6: Checking container logs..."
docker logs --tail 20 $CONTAINER_NAME

echo ""
echo "Step 7: Testing local connection..."
sleep 2
curl -I http://localhost:$PORT

echo ""
echo "=========================================="
echo "Deployment Complete!"
echo "=========================================="
echo "Container is running on port $PORT"
echo "Access it at: http://13.233.90.140:$PORT"
echo ""
echo "Useful commands:"
echo "  docker logs -f $CONTAINER_NAME    # View live logs"
echo "  docker stop $CONTAINER_NAME       # Stop container"
echo "  docker restart $CONTAINER_NAME    # Restart container"
echo "=========================================="
