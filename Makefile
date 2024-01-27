.PHONY: all
all: build-backend build-frontend run-backend run-frontend run-searxng

.PHONY: build-backend
build-backend:
	docker build -t backend-service -f Dockerfile.backend .

.PHONY: build-frontend
build-frontend:
	docker build -t frontend-app -f Dockerfile.frontend .

.PHONY: run-backend
run-backend:
	docker run -d -p 8000:8000 --env-file backend.env backend-service

.PHONY: run-frontend
run-frontend:
	docker run -d -p 3000:3000 frontend-app

.PHONY: run-searxng
run-searxng:
	mkdir -p SearXNG
	docker run --restart=unless-stopped --name="xng" -d -p 8080:8080 -v "${PWD}/SearXNG:/etc/searxng" -e "BASE_URL=http://localhost:8080/" -e "INSTANCE_NAME=xng" searxng/searxng

.PHONY: stop
stop:
	docker stop $(docker ps -aq)

.PHONY: clean
clean:
	docker rm $(docker ps -aq)

.PHONY: clean-images
clean-images:
	docker rmi $(docker images -q)