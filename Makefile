@PHONY: install build-prod run-prod stop-prod clean-all clean-custom

WORKING_DIR := $(shell pwd)

install:
	@echo "Installing netcontrol"
	@echo "Working directory: ${WORKING_DIR}"
	cp langate3000-netcontrol.service /etc/systemd/system/
	sed -i 's|__WORKING_DIR__|${WORKING_DIR}|g' /etc/systemd/system/langate3000-netcontrol.service

build-prod:
	@echo "Building production images"
	docker compose -f docker-compose.yml build

run-prod:
  systemctl start langate2000-netcontrol
	@echo "Running the production stack"
	docker compose -f docker-compose.yml up -d

stop-prod:
	@echo "Stopping the production stack"
	docker compose -f docker-compose.yml down

run-beta:
	@echo "Running the pre-production stack"
	docker compose -f docker-compose-beta.yml up --build -d

stop-beta:
	@echo "Stopping the pre-production stack"
	docker compose -f docker-compose-beta.yml down

clean-all:
	@echo "Removing all images related to the project"
	docker compose -f docker-compose.yml down --rmi all
	docker compose -f docker-compose-beta.yml down --rmi all

clean-custom:
	@echo "Removing all custom images"
	docker compose -f docker-compose.yml down --rmi local
	docker compose -f docker-compose-beta.yml down --rmi local
