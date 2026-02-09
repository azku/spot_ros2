# Makefile for running xhost and docker-compose up

include .env
export

BASE_CONFIG := ./spot_driver/config/spot_ros_example.yaml
OUT_CONFIG  := ./secrets/spot.yaml

.PHONY: xhost run

# Default target
all: xhost up

xhost:
	@echo "Running xhost +local:docker"
	@xhost +local:docker

up: $(OUT_CONFIG)
	docker compose up

$(OUT_CONFIG): $(BASE_CONFIG)
	@mkdir -p secrets
	@echo "Generating Spot config with secrets"
	@cp $(BASE_CONFIG) $(OUT_CONFIG)
	@echo "" >> $(OUT_CONFIG)
	@echo "# ---- injected secrets ----" >> $(OUT_CONFIG)
	@echo "    hostname: \"$(SPOT_HOSTNAME)\"" >> $(OUT_CONFIG)
	@echo "    username: \"$(SPOT_USERNAME)\"" >> $(OUT_CONFIG)
	@echo "    password: \"$(SPOT_PASSWORD)\"" >> $(OUT_CONFIG)
	@chmod 600 $(OUT_CONFIG)


build-development:
	@echo "Building"
	@docker compose build --no-cache spot-ros2-development

build-base:
	@echo "Building Base"
	@docker compose build spot-ros2-base

clean:
	rm -f $(OUT_CONFIG)
