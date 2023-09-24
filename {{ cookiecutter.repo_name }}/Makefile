.PHONY: run build push clean all
	#
# Get image IMAGE_VERSIONs from .env file
ifneq (,$(wildcard ./.env))
	include .env
	export
endif
# Set default image IMAGE_VERSIONs if .env file is not present
BASE_IMAGE_IMAGE_VERSION ?= 0.1.0
IMAGE_IMAGE_VERSION ?= 0.1.0

.DEFAULT_GOAL := all

registry_name := {{ cookiecutter.registry_name }}
repo_name := {{ cookiecutter.repo_name }}
build_dir := ./.cache

# copy template.env to .env if .env does not exist
.env:
	cp template.env .env
	include .env
	export

# create build directory
$(build_dir): .env
	mkdir -p $@

$(build_dir)/build_base: Dockerfile.base | $(build_dir)
	docker build \
		--tag $(registry_name)/ml-base:$(BASE_IMAGE_VERSION) \
		--tag $(registry_name)/ml-base:latest \
		-f Dockerfile.base .
	touch $@

$(build_dir)/build: Dockerfile pyproject.toml $(build_dir)/build_base
	docker build \
		--build-arg BASE_IMAGE_VERSION=$(BASE_IMAGE_VERSION) \
		--tag $(registry_name)/$(repo_name):$(IMAGE_VERSION) \
		--tag $(registry_name)/$(repo_name):latest \
		-f Dockerfile .
	touch $@

$(build_dir)/push_base: $(build_dir)/build_base
	docker push -a $(registry_name)/ml-base
	touch $@

$(build_dir)/push: $(build_dir)/build
	docker push -a $(registry_name)/$(repo_name)
	touch $@

build: $(build_dir)/build

push: $(build_dir)/push_base $(build_dir)/push

clean:
	rm -rf $(build_dir)

all: build push

run:
	docker run \
		--mount type=bind,source="$(shell pwd)",target=/home/dev/app \
		--name $(repo_name) \
		--gpus all \
		--ipc host \
		-p 8888:8888 \
		--rm \
		-it \
		$(registry_name)/$(repo_name):$(IMAGE_VERSION)

jupyter: $(build_dir)/build
	docker compose up && docker compose rm -fsv
