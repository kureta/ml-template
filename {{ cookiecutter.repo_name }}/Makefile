.PHONY: init build_base build_app build_dev build_test build push_base push_app push_dev push_test build run jupyter test all clean
.DEFAULT_GOAL := all

# Get image versions from .env file
ifneq (,$(wildcard ./.env))
  include .env
  export
endif

# build cache to store last successful build times
BUILD_DIR := ./.cache
# image names
BASE_IMAGE_NAME := ml-base
IMAGE_NAME := {{ cookiecutter.repo_name }}
TEST_IMAGE_NAME := $(IMAGE_NAME)-test
DEV_IMAGE_NAME := $(IMAGE_NAME)-dev
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

$(BUILD_DIR)/build_base: Dockerfile.base | $(BUILD_DIR)
	docker build \
		--tag $(DOCKER_REGISTRY)/$(BASE_IMAGE_NAME):$(BASE_IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(BASE_IMAGE_NAME):latest \
		-f Dockerfile.base .
	touch $@

$(BUILD_DIR)/build_app: Dockerfile pyproject.toml $(BUILD_DIR)/build_base
	docker build \
		--build-arg BASE_IMAGE_VERSION=$(BASE_IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(IMAGE_NAME):latest \
		-f Dockerfile .
	touch $@

$(BUILD_DIR)/build_test: $(BUILD_DIR)/build_app Dockerfile.test requirements.test.txt
	docker build \
		--build-arg IMAGE_VERSION=$(IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(TEST_IMAGE_NAME):$(IMAGE_VERSION)-test.$(TEST_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(TEST_IMAGE_NAME):latest \
		-f Dockerfile.test .
	touch $@

$(BUILD_DIR)/build_dev: $(BUILD_DIR)/build_app Dockerfile.dev requirements.dev.txt
	docker build \
		--build-arg IMAGE_VERSION=$(IMAGE_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(DEV_IMAGE_NAME):$(IMAGE_VERSION)-test.$(DEV_VERSION) \
		--tag $(DOCKER_REGISTRY)/$(DEV_IMAGE_NAME):latest \
		-f Dockerfile.test .
	touch $@

$(BUILD_DIR)/push_base: $(BUILD_DIR)/build_base
	docker push -a $(DOCKER_REGISTRY)/$(BASE_IMAGE_NAME)
	touch $@

$(BUILD_DIR)/push_app: $(BUILD_DIR)/build_app
	docker push -a $(DOCKER_REGISTRY)/$(IMAGE_NAME)
	touch $@

$(BUILD_DIR)/push_test: $(BUILD_DIR)/build_test
	docker push -a $(DOCKER_REGISTRY)/$(TEST_IMAGE_NAME)
	touch $@

$(BUILD_DIR)/push_dev: $(BUILD_DIR)/build_dev
	docker push -a $(DOCKER_REGISTRY)/$(DEV_IMAGE_NAME)
	touch $@

build_base: $(BUILD_DIR)/build_base
build_app: $(BUILD_DIR)/build_app
build_test: $(BUILD_DIR)/build_test
build_dev: $(BUILD_DIR)/build_dev
push_base: $(BUILD_DIR)/push_base
push_app: $(BUILD_DIR)/push_app
push_test: $(BUILD_DIR)/push_test
push_dev: $(BUILD_DIR)/push_dev

push: push_base push_app push_test push_dev
build: build_base build_app build_test build_dev

run: $(BUILD_DIR)/build_app
	docker run \
		--mount type=bind,source="$(shell pwd)",target=/home/dev/app \
		--name $(IMAGE_NAME) \
		--gpus all \
		--ipc host \
		--rm \
		-it \
		$(DOCKER_REGISTRY)/$(IMAGE_NAME):$(IMAGE_VERSION)

jupyter: $(BUILD_DIR)/build_dev
	docker run \
		--mount type=bind,source="$(shell pwd)",target=/home/dev/app \
		--name $(DEV_IMAGE_NAME) \
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

all: build_base build_app build_test build_dev

clean:
	rm -rf $(BUILD_DIR)
