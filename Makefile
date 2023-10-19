setup:
	@echo "Setting up virtual environment"
	python -m venv .env

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

astro-init:
	@echo "Init Astro"	
	cd src/airflow/ && astro dev init 

astro-start:
	@echo "Starting airflow components containers"
	cd src/airflow/ && astro dev start

astro-restart:
	@echo "Restarting airflow containers"
	astro dev restart

astro-stop:
	@echo "Stopping airflow components containers"
	astro dev stop

astro-ps:
	@echo "Listing all Docker containers running"
	astro dev ps

webserver-port:
	@echo "Set the airflow webserver port"
	astro config set webserver.port 8080

all: install lint test