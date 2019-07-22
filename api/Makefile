.PHONY: all clean
all: build_docker
build_docker: 
	docker login
	docker build --no-cache -t api_docker:latest .
	docker tag api_docker ttw225/api_docker
	docker push ttw225/api_docker
