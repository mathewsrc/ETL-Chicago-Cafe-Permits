setup:
	@echo "Setting up virtual environment"
	python -m venv ~/.env

install:
	@echo "Installing dependencies"
	pip install --upgrade pip  &&\
		pip install -r requirements.txt

format:
	@echo "Formatting all projects with black"
	./format.sh

lint:
	@echo "Linting all projects with ruff"
	./lint.sh

test:
	@echo "Testing all projects with pytest"
	./test.sh

docker-build:
	@echo "Building Docker image"
	docker build -t webapp .

docker-run:
	@echo "Running Docker image"
	docker run webapp 

docker-images:
	@echo "List all images"
	docker images

docker-clean-images:
	@echo "remove all images locally"
	if [ -n "$$(docker images -aq)" ]; then \
		docker rmi -f $$(docker images -aq); \
	fi

docker-containers:
	@echo "List all containers"
	docker ps -a

docker-clean-containers:
	@echo "remove all containers locally"
	if [ -n "$$(docker ps -aq)" ]; then \
		docker rm -f $$(docker ps -aq); \
	fi

login:
	@echo "Logging in to Hugging Face"
	huggingface-cli login

logout:
	@echo "Logging out of Hugging Face"
	huggingface-cli logout



all: install lint test