.PHONY: run build push clean all
.DEFAULT_GOAL := all

registry_name := {{ cookiecutter.registry_name }}
repo_name := {{ cookiecutter.repo_name }}
base_version := 0.1.0
version := 0.1.0
build_dir := ./.cache

$(build_dir):
	mkdir -p $@

$(build_dir)/build_base: Dockerfile.base | $(build_dir)
	docker build \
		--tag $(registry_name)/ml-base:$(base_version) \
		--tag $(registry_name)/ml-base:latest \
		-f Dockerfile.base .
	touch $@

$(build_dir)/build: Dockerfile pyproject.toml $(build_dir)/build_base
	docker build \
		--tag $(registry_name)/$(repo_name):$(version) \
		--tag $(registry_name)/$(repo_name):latest \
		-f Dockerfile .
	touch $@

$(build_dir)/push_base: $(build_dir)/build_base
	docker push -a $(registry_name)/ml-base
	touch $@

$(build_dir)/push: $(build_dir)/build
	docker push -a $(registry_name)/$(repo_name)
	touch $@

build: $(build_dir)/build_base $(build_dir)/build

push: $(build_dir)/push_base $(build_dir)/push

clean:
	rm -rf $(build_dir)

all: build push

run:
	docker run \
		--mount type=bind,source="$(shell pwd)",target=/home/developer/app \
		--name $(repo_name) \
		--gpus all \
		--ipc host \
		-p 8888:8888 \
		--rm \
		-it \
		$(registry_name)/$(repo_name):$(version)
