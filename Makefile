# Makefile for running xhost and docker-compose up

.PHONY: setup run

# Default target
all: setup run

setup:
	@echo "Running xhost +local:docker"
	@xhost +local:docker

run:
	@echo "Starting Docker Compose"
	@docker compose up

build-development:
	@echo "Building"
	@docker compose build --no-cache spot-ros2-development

build-base:
	@echo "Building Base"
	@docker compose build spot-ros2-base

