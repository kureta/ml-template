# set MLFLOW_TRACKING_URI, MLFLOW_TRACKING_USERNAME, MLFLOW_TRACKING_PASSWORD
# make an mlflow action
.PHONY: init build_base build build_test push run jupyter test all clean
.DEFAULT_GOAL := all

# Get image versions from .env file
ifneq (,$(wildcard ./.env))
  include .env
  export
endif

# build cache to store last successful build times
BUILD_DIR := ./.cache
# venv for installing pre-commit and nbstripout
VENV_ACTIVATE = . .venv/bin/activate
# image names
BASE_IMAGE_NAME := ml-base
IMAGE_NAME := {{ cookiecutter.repo_name }}
TEST_IMAGE_NAME := $(IMAGE_NAME)-test
# docker repository to push the image
DOCKER_REGISTRY := {{ cookiecutter.registry_name }}

# copy template.env to .env if .env does not exist
.env:
	cp template.env .env
  include .env
  export

# create build directory
$(BUILD_DIR): .env
	mkdir -p $@

# initialize development tools at the host machine
.venv: requirements.dev.txt
	rm -rf .venv
	python -m venv .venv
	$(VENV_ACTIVATE) && \
	pip install -r requirements.dev.txt

$(BUILD_DIR)/init: .venv $(BUILD_DIR)
	$(VENV_ACTIVATE) && \
	pre-commit install && \
	nbstripout --install
	touch $@

.git:
	git init

.dvc:
	$(VENV_ACTIVATE) && \
	dvc init && \
	dvc remote add -d storage {{ cookiecutter.dvc_bucket }} && \
	dvc remote modify storage endpointurl {{ cookiecutter.dvc_endpoint }} && \
	dvc config core.autostage true && \
	dvc config core.analytics false

init: .git $(BUILD_DIR)/init .dvc

$(BUILD_DIR)/build_base: Dockerfile.base | $(BUILD_DIR)
	docker build \
		--tag $(DOCKER_REGISTRY)/$(BASE_IMAGE_NAME):$(BASE_IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(BASE_IMAGE_NAME):latest \
		-f Dockerfile.base .
	touch $@

$(BUILD_DIR)/build: Dockerfile pyproject.toml $(BUILD_DIR)/build_base
	docker build \
		--build-arg BASE_IMAGE_VERSION=$(BASE_IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(IMAGE_NAME):latest \
		-f Dockerfile .
	touch $@

$(BUILD_DIR)/build_test: $(BUILD_DIR)/build Dockerfile.test requirements.test.txt
	docker build \
		--build-arg IMAGE_VERSION=$(IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(TEST_IMAGE_NAME):$(IMAGE_VERSION)-test.$(TEST_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(TEST_IMAGE_NAME):latest \
		-f Dockerfile.test .
	touch $@

$(BUILD_DIR)/push_base: $(BUILD_DIR)/build_base
	docker push -a $(DOCKER_REGISTRY)/$(BASE_IMAGE_NAME)
	touch $@

$(BUILD_DIR)/push: $(BUILD_DIR)/build
	docker push -a $(DOCKER_REGISTRY)/$(IMAGE_NAME)
	touch $@

$(BUILD_DIR)/push_test: $(BUILD_DIR)/build_test
	docker push -a $(DOCKER_REGISTRY)/$(TEST_IMAGE_NAME)
	touch $@

build_base: $(BUILD_DIR)/build_base

build: $(BUILD_DIR)/build

build_test: $(BUILD_DIR)/build_test

push: $(BUILD_DIR)/push_base $(BUILD_DIR)/push $(BUILD_DIR)/push_test

run: $(BUILD_DIR)/build
	docker run \
		--mount type=bind,source="$(shell pwd)",target=/home/dev/app \
		--name $(IMAGE_NAME) \
		--gpus all \
		--ipc host \
		--rm \
		-it \
		$(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION)

jupyter: $(BUILD_DIR)/build
	docker run \
		--mount type=bind,source="$(shell pwd)",target=/home/dev/app \
		--name $(IMAGE_NAME)-jupyter \
		--gpus all \
		--ipc host \
		-p 8888:8888 \
		--rm \
		$(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION) \
		jupyter lab --no-browser --ip "*"

test: $(BUILD_DIR)/build_test
	docker run \
		--mount type=bind,source="$(shell pwd)",target=/home/dev/app \
		--name $(TEST_IMAGE_NAME) \
		--gpus all \
		--ipc host \
		--rm \
		$(DOCKER_REGISTRY)/$(TEST_IMAGE_NAME):$(IMAGE_VERSION)-test.$(TEST_VERSION) \
		cowsay -t "All tests passed!"

all: build_base build build_test

clean:
	rm -rf $(BUILD_DIR)
