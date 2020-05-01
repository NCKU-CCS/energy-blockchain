.PHONY: all clean
all: build_ami_docker
build_ami_docker:
	pipenv lock --requirements > ami/requirements.txt
	docker build -t uploader:latest ami/ --no-cache
