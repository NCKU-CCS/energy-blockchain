.PHONY: all clean
all: build_docker
build_docker: 
	pipenv lock --requirements > api/requirements.txt
	docker login
	docker build --no-cache -t api_docker:latest api/
	docker tag api_docker ttw225/api_docker
	docker push ttw225/api_docker
