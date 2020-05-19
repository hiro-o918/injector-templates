IMAGE_NAME := injector-templates
CONTAINER_NAME := injector-templates
WORKINGDIR := /app


.PHONY: build
build:
	@docker build -t $(IMAGE_NAME) .

.PHONY: run
run:
	@docker run \
		--rm -it \
		${DOCKER_GPU_PARAMS} \
		--name $(CONTAINER_NAME) \
		--volume $(CURDIR):$(WORKINGDIR) \
		--publish 8888:8888 \
		$(IMAGE_NAME) \
		${ARGS}

.PHONY: bash
bash: ARGS=bash
export ARGS
bash:
	@${MAKE} run

.PHONY: lint
lint: ARGS=flake8 lab
export ARGS
lint:
	@${MAKE} run

.PHONY: isort
isort: ARGS=isort -rc lab
export ARGS
isort:
	@${MAKE} run