# Define variables
IMAGE_NAME = rule-based-role
CONTAINER_NAME = rule-based-role
DOCKERFILE_PATH = .

# Build the Docker image
build:
	docker build -t $(IMAGE_NAME) $(DOCKERFILE_PATH)

# Run the Docker container
run:
	docker run --name $(CONTAINER_NAME) $(IMAGE_NAME)

# View logs of the running container
logs:
	docker logs $(CONTAINER_NAME)

# Access the running container with a bash shell
shell:
	docker exec -it $(CONTAINER_NAME) /bin/bash

# Stop and remove the running container
clean:
	docker stop $(CONTAINER_NAME) || true
	docker rm $(CONTAINER_NAME) || true

# Remove Docker image
remove-image:
	docker rmi $(IMAGE_NAME) || true

# Rebuild and run the Docker container (clean build)
rebuild: clean build run

# Clean up everything (containers and image)
clean-all: clean remove-image

# Full rebuild from scratch and show the output of the Python program
full-rebuild: clean-all build
	docker run --name $(CONTAINER_NAME) $(IMAGE_NAME)

.PHONY: build run logs shell clean rebuild remove-image clean-all full-rebuild
