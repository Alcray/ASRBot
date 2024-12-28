#!/bin/bash

# Define the image and container names
IMAGE_NAME="armenian-asr-bot"
CONTAINER_NAME="armenian-asr-bot"
DOCKERFILE_PATH="Dockerfile" # Path to the Dockerfile

# Build the Docker image using the specified Dockerfile
echo "Building the Docker image..."
docker build -t $IMAGE_NAME -f $DOCKERFILE_PATH .

# Stop and remove any existing container with the same name
if [ $(docker ps -aq -f name=$CONTAINER_NAME) ]; then
    echo "Stopping and removing the existing container..."
    docker stop $CONTAINER_NAME
    docker rm $CONTAINER_NAME
fi

# Run the Docker container
echo "Running the Docker container..."
docker run --gpus all --restart unless-stopped -d \
    -v $(pwd)/config:/app/config \
    -v $(pwd)/workspace:/app/workspace \
    --name $CONTAINER_NAME $IMAGE_NAME

# Confirm the container is running
if [ $(docker ps -q -f name=$CONTAINER_NAME) ]; then
    echo "The Docker container '$CONTAINER_NAME' is now running."
else
    echo "Failed to start the Docker container."
fi
